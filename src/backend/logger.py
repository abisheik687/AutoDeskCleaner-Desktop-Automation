"""Logger for AutoDeskCleaner"""
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class Logger:
    """Tracks and logs all file operations"""
    
    def __init__(self):
        """Initialize Logger"""
        self.operations: List[Dict] = []
        self.stats = {
            "total_files": 0,
            "moved": 0,
            "skipped": 0,
            "failed": 0,
            "categories": {}
        }
    
    def log_operation(self, operation: Dict) -> None:
        """Log a file operation"""
        self.operations.append(operation)
        
        # Update statistics
        self.stats["total_files"] += 1
        
        status = operation.get("status", "")
        if status == "success":
            self.stats["moved"] += 1
            category = operation.get("category", "Others")
            self.stats["categories"][category] = self.stats["categories"].get(category, 0) + 1
        elif status == "skipped":
            self.stats["skipped"] += 1
        elif status == "failed":
            self.stats["failed"] += 1
    
    def log_error(self, filepath: str, error: str, category: str = "") -> None:
        """Log an error for a specific file"""
        operation = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": filepath,
            "destination": "",
            "category": category,
            "status": "failed",
            "error": error
        }
        self.log_operation(operation)
    
    def log_success(self, source: str, destination: str, category: str) -> None:
        """Log a successful file move"""
        operation = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": source,
            "destination": destination,
            "category": category,
            "status": "success",
            "error": ""
        }
        self.log_operation(operation)
    
    def log_skip(self, filepath: str, reason: str, category: str = "") -> None:
        """Log a skipped file"""
        operation = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": filepath,
            "destination": "",
            "category": category,
            "status": "skipped",
            "error": reason
        }
        self.log_operation(operation)
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return self.stats.copy()
    
    def display_summary(self) -> None:
        """Display summary to console"""
        print("\n" + "="*60)
        print("CLEANUP SUMMARY")
        print("="*60)
        print(f"Total files processed: {self.stats['total_files']}")
        print(f"Successfully moved: {self.stats['moved']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Failed: {self.stats['failed']}")
        
        if self.stats['categories']:
            print("\nFiles by category:")
            for category, count in sorted(self.stats['categories'].items()):
                print(f"  {category}: {count}")
        
        print("="*60 + "\n")
    
    def write_to_file(self, log_path: str) -> None:
        """Write operations log to file"""
        try:
            # Create log directory if needed
            log_dir = os.path.dirname(log_path)
            if log_dir:
                Path(log_dir).mkdir(parents=True, exist_ok=True)
            
            # Append to log file
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"Cleanup Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*60}\n\n")
                
                for op in self.operations:
                    f.write(f"[{op['timestamp']}] {op['status'].upper()}\n")
                    f.write(f"  Source: {op['source']}\n")
                    if op['destination']:
                        f.write(f"  Destination: {op['destination']}\n")
                    if op['category']:
                        f.write(f"  Category: {op['category']}\n")
                    if op['error']:
                        f.write(f"  Error: {op['error']}\n")
                    f.write("\n")
                
                # Write summary
                f.write(f"\nSummary:\n")
                f.write(f"  Total: {self.stats['total_files']}, ")
                f.write(f"Moved: {self.stats['moved']}, ")
                f.write(f"Skipped: {self.stats['skipped']}, ")
                f.write(f"Failed: {self.stats['failed']}\n")
                f.write(f"{'='*60}\n")
        
        except Exception as e:
            print(f"Warning: Could not write to log file: {e}")
