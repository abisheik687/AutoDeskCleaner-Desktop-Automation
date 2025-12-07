"""Flask API for AutoDeskCleaner Web Interface"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config_manager import ConfigManager
from scanner import Scanner
from categorizer import Categorizer
from mover import Mover
from logger import Logger

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Global instances
config_manager = ConfigManager("config.json")
logger = Logger()


@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/scan', methods=['GET'])
def scan_desktop():
    """Scan desktop and return file list with categories"""
    try:
        config_manager.load_config()
        desktop_path = str(Path(config_manager.get_desktop_path()).expanduser())
        system_files = config_manager.get_system_files()
        categories = config_manager.get_categories()
        
        scanner = Scanner(system_files)
        categorizer = Categorizer(categories)
        
        files = scanner.scan_desktop(desktop_path)
        
        # Categorize files
        file_data = []
        category_counts = {}
        
        for filepath in files:
            filename = os.path.basename(filepath)
            category = categorizer.categorize_file(filepath)
            extension = scanner.get_file_extension(filepath)
            
            file_data.append({
                "path": filepath,
                "name": filename,
                "category": category,
                "extension": extension
            })
            
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return jsonify({
            "success": True,
            "files": file_data,
            "total": len(files),
            "categories": category_counts
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/preview', methods=['POST'])
def preview_cleanup():
    """Preview what cleanup would do"""
    try:
        data = request.json
        files = data.get('files', [])
        
        config_manager.load_config()
        target_base = str(Path(config_manager.get_target_base_path()).expanduser())
        
        preview_data = []
        for file_info in files:
            filepath = file_info['path']
            category = file_info['category']
            filename = os.path.basename(filepath)
            destination = os.path.join(target_base, category, filename)
            
            preview_data.append({
                "source": filepath,
                "destination": destination,
                "category": category,
                "filename": filename
            })
        
        return jsonify({
            "success": True,
            "preview": preview_data
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/cleanup', methods=['POST'])
def execute_cleanup():
    """Execute the cleanup operation"""
    try:
        data = request.json
        files = data.get('files', [])
        
        config_manager.load_config()
        target_base = str(Path(config_manager.get_target_base_path()).expanduser())
        log_file = str(Path(config_manager.get_log_file()).expanduser())
        
        mover = Mover()
        global logger
        logger = Logger()
        
        results = []
        for file_info in files:
            filepath = file_info['path']
            category = file_info['category']
            filename = os.path.basename(filepath)
            
            success, destination, error = mover.move_file(filepath, category, target_base)
            
            if success:
                logger.log_success(filepath, destination, category)
                results.append({
                    "filename": filename,
                    "status": "success",
                    "destination": destination
                })
            else:
                logger.log_error(filepath, error, category)
                results.append({
                    "filename": filename,
                    "status": "failed",
                    "error": error
                })
        
        # Write log
        logger.write_to_file(log_file)
        
        return jsonify({
            "success": True,
            "results": results,
            "summary": logger.get_summary()
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get recent operation logs"""
    try:
        config_manager.load_config()
        log_file = str(Path(config_manager.get_log_file()).expanduser())
        
        if not os.path.exists(log_file):
            return jsonify({"success": True, "logs": ""})
        
        # Read last 100 lines
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            recent_logs = ''.join(lines[-100:])
        
        return jsonify({
            "success": True,
            "logs": recent_logs
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/config', methods=['GET', 'POST'])
def manage_config():
    """Get or update configuration"""
    try:
        if request.method == 'GET':
            config_manager.load_config()
            return jsonify({
                "success": True,
                "config": config_manager.config
            })
        
        else:  # POST
            new_config = request.json
            
            # Validate and save
            with open("config.json", 'w', encoding='utf-8') as f:
                import json
                json.dump(new_config, f, indent=2)
            
            config_manager.load_config()
            
            return jsonify({
                "success": True,
                "message": "Configuration updated successfully"
            })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current statistics"""
    return jsonify({
        "success": True,
        "stats": logger.get_summary()
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
