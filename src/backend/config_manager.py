"""Configuration Manager for AutoDeskCleaner"""
import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Manages configuration loading, validation, and default creation"""
    
    DEFAULT_CONFIG = {
        "desktop_path": str(Path.home() / "Desktop"),
        "target_base_path": str(Path.home() / "Desktop" / "Organized"),
        "categories": {
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".odt", ".rtf"],
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".webp"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Code": [".py", ".js", ".java", ".cpp", ".c", ".h", ".html", ".css", ".json", ".xml"]
        },
        "system_files": ["desktop.ini", ".DS_Store", "thumbs.db", "Thumbs.db"],
        "log_file": str(Path.home() / "Desktop" / "Organized" / "cleanup_log.txt")
    }
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize ConfigManager with config file path"""
        self.config_path = config_path
        self.config = None
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if not os.path.exists(self.config_path):
            self.create_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return self.config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
        except Exception as e:
            raise IOError(f"Error reading configuration file: {e}")
    
    def create_default_config(self) -> None:
        """Create default configuration file"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.DEFAULT_CONFIG, f, indent=2)
            self.config = self.DEFAULT_CONFIG.copy()
        except Exception as e:
            raise IOError(f"Error creating default configuration: {e}")
    
    def get_categories(self) -> Dict[str, list]:
        """Get file categories mapping"""
        if self.config is None:
            self.load_config()
        return self.config.get("categories", {})
    
    def get_desktop_path(self) -> str:
        """Get desktop directory path"""
        if self.config is None:
            self.load_config()
        return self.config.get("desktop_path", str(Path.home() / "Desktop"))
    
    def get_target_base_path(self) -> str:
        """Get target base directory path"""
        if self.config is None:
            self.load_config()
        return self.config.get("target_base_path", str(Path.home() / "Desktop" / "Organized"))
    
    def get_system_files(self) -> list:
        """Get list of system files to exclude"""
        if self.config is None:
            self.load_config()
        return self.config.get("system_files", [])
    
    def get_log_file(self) -> str:
        """Get log file path"""
        if self.config is None:
            self.load_config()
        return self.config.get("log_file", str(Path.home() / "Desktop" / "Organized" / "cleanup_log.txt"))
