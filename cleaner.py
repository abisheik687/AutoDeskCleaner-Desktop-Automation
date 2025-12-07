"""AutoDeskCleaner - Automated Desktop File Organizer"""
import sys
import argparse
from pathlib import Path

# Add src/backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from config_manager import ConfigManager
from scanner import Scanner
from categorizer import Categorizer
from mover import Mover
from logger import Logger


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="AutoDeskCleaner - Automatically organize your desktop files"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without moving files"
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("AutoDeskCleaner - Desktop File Organizer")
    print("="*60 + "\n")
    
    # Initialize components
    try:
        # Load configuration
        print(f"Loading configuration from {args.config}...")
        config_manager = ConfigManager(args.config)
        config_manager.load_config()
        
        desktop_path = config_manager.get_desktop_path()
        target_base = config_manager.get_target_base_path()
        categories = config_manager.get_categories()
        system_files = config_manager.get_system_files()
        log_file = config_manager.get_log_file()
        
        # Expand user paths
        desktop_path = str(Path(desktop_path).expanduser())
        target_base = str(Path(target_base).expanduser())
        log_file = str(Path(log_file).expanduser())
        
        print(f"Desktop path: {desktop_path}")
        print(f"Target path: {target_base}")
        
        if args.dry_run:
            print("\n*** DRY RUN MODE - No files will be moved ***\n")
        
        # Initialize modules
        scanner = Scanner(system_files)
        categorizer = Categorizer(categories)
        mover = Mover()
        logger = Logger()
        
        # Scan desktop
        print("\nScanning desktop...")
        files = scanner.scan_desktop(desktop_path)
        print(f"Found {len(files)} files to process")
        
        if len(files) == 0:
            print("\nNo files to organize. Desktop is clean!")
            return
        
        # Process each file
        print("\nProcessing files...")
        for filepath in files:
            filename = Path(filepath).name
            
            # Categorize
            category = categorizer.categorize_file(filepath)
            
            if args.dry_run:
                # Dry run - just preview
                print(f"  [{category}] {filename}")
                logger.log_success(filepath, f"{target_base}/{category}/{filename}", category)
            else:
                # Actually move the file
                success, destination, error = mover.move_file(filepath, category, target_base)
                
                if success:
                    print(f"  ✓ [{category}] {filename}")
                    logger.log_success(filepath, destination, category)
                else:
                    print(f"  ✗ [{category}] {filename} - {error}")
                    logger.log_error(filepath, error, category)
        
        # Display summary
        logger.display_summary()
        
        # Write to log file
        if not args.dry_run:
            logger.write_to_file(log_file)
            print(f"Log written to: {log_file}")
        
        print("\nCleanup complete!")
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("Please check your config.json file for valid JSON syntax.")
        sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    except PermissionError as e:
        print(f"\n❌ Permission Error: {e}")
        print("Please check file and directory permissions.")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
