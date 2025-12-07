"""File Categorizer for AutoDeskCleaner"""
import os
from typing import Dict, List


class Categorizer:
    """Categorizes files based on extension mapping"""
    
    def __init__(self, categories: Dict[str, List[str]]):
        """Initialize Categorizer with category mappings"""
        self.categories = categories
        # Create reverse mapping for faster lookup: extension -> category
        self.extension_map = {}
        for category, extensions in categories.items():
            for ext in extensions:
                # Normalize extensions to lowercase
                self.extension_map[ext.lower()] = category
    
    def categorize_file(self, filepath: str) -> str:
        """Categorize a file based on its extension"""
        extension = self.get_file_extension(filepath)
        return self.get_category_for_extension(extension)
    
    def get_category_for_extension(self, extension: str) -> str:
        """Get category for a given extension"""
        # Normalize extension to lowercase
        extension = extension.lower()
        
        # Ensure extension starts with dot
        if extension and not extension.startswith('.'):
            extension = '.' + extension
        
        # Return mapped category or default "Others"
        return self.extension_map.get(extension, "Others")
    
    def get_file_extension(self, filepath: str) -> str:
        """Extract file extension from filepath"""
        filename = os.path.basename(filepath)
        
        # Handle files without extension
        if '.' not in filename:
            return ""
        
        # Get extension after last dot
        extension = os.path.splitext(filename)[1]
        return extension.lower()
