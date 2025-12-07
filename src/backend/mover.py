"""File Mover for AutoDeskCleaner"""
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Tuple


class Mover:
    """Handles file movement operations with error handling"""
    
    def move_file(self, source: str, category: str, base_path: str) -> Tuple[bool, str, str]:
        """
        Move file to categorized folder
        Returns: (success, destination_path, error_message)
        """
        try:
            # Create target directory
            target_dir = os.path.join(base_path, category)
            if not self.create_target_directory(target_dir):
                return False, "", f"Failed to create directory: {target_dir}"
            
            # Get filename and construct target path
            filename = os.path.basename(source)
            target_path = os.path.join(target_dir, filename)
            
            # Handle duplicates
            if os.path.exists(target_path):
                target_path = self.handle_duplicate(target_path)
            
            # Move the file
            shutil.move(source, target_path)
            return True, target_path, ""
        
        except PermissionError as e:
            return False, "", f"Permission denied: {str(e)}"
        except OSError as e:
            if "being used by another process" in str(e).lower():
                return False, "", f"File in use by another process: {str(e)}"
            return False, "", f"OS error: {str(e)}"
        except Exception as e:
            return False, "", f"Unexpected error: {str(e)}"
    
    def create_target_directory(self, directory_path: str) -> bool:
        """Create target directory if it doesn't exist"""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except PermissionError:
            return False
        except Exception:
            return False
    
    def handle_duplicate(self, target_path: str) -> str:
        """Handle duplicate files by adding timestamp suffix"""
        directory = os.path.dirname(target_path)
        filename = os.path.basename(target_path)
        name, ext = os.path.splitext(filename)
        
        timestamp = self.generate_timestamp_suffix()
        new_filename = f"{name}_{timestamp}{ext}"
        return os.path.join(directory, new_filename)
    
    def generate_timestamp_suffix(self) -> str:
        """Generate timestamp suffix for duplicate files"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
