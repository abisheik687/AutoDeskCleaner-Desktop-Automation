"""Quick test script for AutoDeskCleaner"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "src" / "backend"))

from config_manager import ConfigManager
from scanner import Scanner
from categorizer import Categorizer
from mover import Mover
from logger import Logger


def create_test_files():
    """Create test files for demonstration"""
    test_dir = Path("test_desktop")
    test_dir.mkdir(exist_ok=True)
    
    # Create sample files
    test_files = [
        "report.pdf", "document.docx", "notes.txt",
        "photo1.jpg", "photo2.png", "screenshot.gif",
        "video.mp4", "movie.avi",
        "song.mp3", "audio.wav",
        "archive.zip", "backup.tar",
        "script.py", "app.js", "style.css"
    ]
    
    for filename in test_files:
        filepath = test_dir / filename
        filepath.write_text(f"Test content for {filename}")
    
    print(f"✓ Created {len(test_files)} test files in {test_dir}")
    return str(test_dir)


def test_scanner():
    """Test Scanner module"""
    print("\n=== Testing Scanner ===")
    scanner = Scanner()
    
    test_dir = create_test_files()
    files = scanner.scan_desktop(test_dir)
    
    print(f"✓ Found {len(files)} files")
    for f in files[:3]:
        print(f"  - {Path(f).name}")
    print(f"  ... and {len(files) - 3} more")
    
    return files


def test_categorizer(files):
    """Test Categorizer module"""
    print("\n=== Testing Categorizer ===")
    
    config = ConfigManager()
    config.load_config()
    categories = config.get_categories()
    
    categorizer = Categorizer(categories)
    
    category_counts = {}
    for filepath in files:
        category = categorizer.categorize_file(filepath)
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("✓ Categorization complete:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count} files")
    
    return category_counts


def test_logger():
    """Test Logger module"""
    print("\n=== Testing Logger ===")
    
    logger = Logger()
    
    # Simulate some operations
    logger.log_success("/test/file1.pdf", "/organized/Documents/file1.pdf", "Documents")
    logger.log_success("/test/photo.jpg", "/organized/Images/photo.jpg", "Images")
    logger.log_error("/test/locked.doc", "Permission denied", "Documents")
    
    summary = logger.get_summary()
    print(f"✓ Total: {summary['total_files']}")
    print(f"✓ Moved: {summary['moved']}")
    print(f"✓ Failed: {summary['failed']}")


def test_config():
    """Test ConfigManager module"""
    print("\n=== Testing ConfigManager ===")
    
    config = ConfigManager()
    config.load_config()
    
    print(f"✓ Desktop path: {config.get_desktop_path()}")
    print(f"✓ Target path: {config.get_target_base_path()}")
    print(f"✓ Categories: {len(config.get_categories())}")
    print(f"✓ System files: {len(config.get_system_files())}")


def cleanup_test_files():
    """Remove test files"""
    import shutil
    test_dir = Path("test_desktop")
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print("\n✓ Cleaned up test files")


def main():
    """Run all tests"""
    print("="*60)
    print("AutoDeskCleaner - Quick Test Suite")
    print("="*60)
    
    try:
        # Test individual modules
        test_config()
        files = test_scanner()
        test_categorizer(files)
        test_logger()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cleanup_test_files()


if __name__ == "__main__":
    main()
