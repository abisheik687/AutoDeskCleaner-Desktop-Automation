# 🚀 AutoDeskCleaner - Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Python
If you don't have Python installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac**: `brew install python3`
- **Linux**: `sudo apt install python3 python3-pip`

Verify installation:
```bash
python --version
# Should show Python 3.8 or higher
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 (Web framework)
- flask-cors 4.0.0 (CORS support)

### Step 3: Test the Installation
```bash
python test_cleaner.py
```

Expected output:
```
============================================================
AutoDeskCleaner - Quick Test Suite
============================================================

=== Testing ConfigManager ===
✓ Desktop path: C:\Users\YourName\Desktop
✓ Target path: C:\Users\YourName\Desktop\Organized
✓ Categories: 6
✓ System files: 4

=== Testing Scanner ===
✓ Created 15 test files in test_desktop
✓ Found 15 files
  - report.pdf
  - document.docx
  - notes.txt
  ... and 12 more

=== Testing Categorizer ===
✓ Categorization complete:
  Archives: 2 files
  Audio: 2 files
  Code: 3 files
  Documents: 3 files
  Images: 3 files
  Videos: 2 files

=== Testing Logger ===
✓ Total: 3
✓ Moved: 2
✓ Failed: 1

============================================================
✅ All tests passed!
============================================================
```

---

## Usage Options

### Option 1: CLI Mode (Fastest)

**Dry Run (Preview Only)**
```bash
python cleaner.py --dry-run
```

**Actual Cleanup**
```bash
python cleaner.py
```

**Custom Config**
```bash
python cleaner.py --config my_config.json
```

### Option 2: Web Interface (Recommended)

**Start the Server**
```bash
python src/api/app.py
```

**Open Browser**
```
http://localhost:5000
```

**Use the Interface**
1. Click "Scan Desktop" to see all files
2. Review categorization and statistics
3. Click "Clean Up Now" to organize
4. View logs and modify configuration

---

## First Time Setup

### 1. Customize Configuration (Optional)

Edit `config.json` to match your preferences:

```json
{
  "desktop_path": "~/Desktop",
  "target_base_path": "~/Desktop/Organized",
  "categories": {
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"],
    "Code": [".py", ".js", ".java", ".html"]
  }
}
```

### 2. Test with Dry Run

Always test first:
```bash
python cleaner.py --dry-run
```

This shows what would happen without actually moving files.

### 3. Run Actual Cleanup

When ready:
```bash
python cleaner.py
```

---

## Common Commands

### CLI Commands
```bash
# Help
python cleaner.py --help

# Dry run
python cleaner.py --dry-run

# Custom config
python cleaner.py --config custom.json

# Run tests
python test_cleaner.py
```

### Web Server
```bash
# Start server
python src/api/app.py

# Start on different port
python src/api/app.py --port 8080

# Debug mode
python src/api/app.py --debug
```

---

## Troubleshooting

### Issue: "Python not found"
**Solution**: Install Python from python.org or use `python3` instead of `python`

### Issue: "Module not found"
**Solution**: Install dependencies: `pip install -r requirements.txt`

### Issue: "Permission denied"
**Solution**: Run with administrator privileges or check file permissions

### Issue: "Port 5000 already in use"
**Solution**: Stop other applications using port 5000 or use different port

### Issue: "Desktop path not found"
**Solution**: Update `desktop_path` in config.json to match your system

---

## What Happens During Cleanup?

### Before
```
Desktop/
├── report.pdf
├── photo.jpg
├── video.mp4
├── song.mp3
├── code.py
└── ... (40 more files)
```

### After
```
Desktop/
└── Organized/
    ├── Documents/
    │   └── report.pdf
    ├── Images/
    │   └── photo.jpg
    ├── Videos/
    │   └── video.mp4
    ├── Audio/
    │   └── song.mp3
    └── Code/
        └── code.py
```

### Log File
```
Desktop/Organized/cleanup_log.txt
```

Contains detailed records of all operations.

---

## Scheduling Automatic Cleanup

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Name: "AutoDeskCleaner Daily"
4. Trigger: Daily at 9:00 AM
5. Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\AutoDeskCleaner\cleaner.py`
   - Start in: `C:\path\to\AutoDeskCleaner`
6. Finish

### Mac/Linux (cron)

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /path/to/AutoDeskCleaner && python cleaner.py

# Save and exit
```

---

## Next Steps

1. ✅ Install and test
2. ✅ Customize configuration
3. ✅ Run dry-run
4. ✅ Execute cleanup
5. ✅ Set up scheduling
6. ✅ Enjoy clean desktop!

---

## Need Help?

- **Documentation**: See README.md
- **Issues**: Check SUBMISSION_CHECKLIST.md
- **Blog**: Read BLOG_ARTICLE.md for detailed explanation

---

**Happy Organizing! 🎉**
