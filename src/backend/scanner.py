"""Desktop Scanner for AutoDeskCleaner"""
import os
from pathlib import Path
from typing import List


class Scanner:
    """Scans desktop directory and identifies files for processing"""
    
    def __init__(self, system_files: List[str] = None):
        """Initialize Scanner with system files to exclude"""
        self.system_files = system_files or ["desktop.ini", ".DS_Store", "thumbs.db", "Thumbs.db"]
    
    def scan_desktop(self, desktop_path: str) -> List[str]:
        """Scan desktop directory and return list of processable files"""
        files = []
        
        if not os.path.exists(desktop_path):
            raise FileNotFoundError(f"Desktop path does not exist: {desktop_path}")
        
        try:
            for item in os.listdir(desktop_path):
                item_path = os.path.join(desktop_path, item)
                
                # Skip directories
                if os.path.isdir(item_path):
                    continue
                
                # Skip hidden files
                if self.is_hidden_file(item):
                    continue
                
                # Skip system files
                if self.is_system_file(item):
                    continue
                
                files.append(item_path)
        
        except PermissionError:
            raise PermissionError(f"Permission denied accessing: {desktop_path}")
        
        return files
    
    def is_system_file(self, filename: str) -> bool:
        """Check if file is a system file"""
        return filename in self.system_files
    
    def is_hidden_file(self, filename: str) -> bool:
        """Check if file is hidden (starts with dot on Unix)"""
        return filename.startswith('.')
    
    def get_file_extension(self, filepath: str) -> str:
        """Extract file extension from filepath"""
        filename = os.path.basename(filepath)
        
        # Handle files without extension
        if '.' not in filename:
            return ""
        
        # Get extension after last dot
        extension = os.path.splitext(filename)[1]
        return extension.lower()  # Return lowercase for case-insensitive matching
