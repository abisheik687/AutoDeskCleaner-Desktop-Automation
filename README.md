# 🗂️ AutoDeskCleaner

**Automated Desktop File Organization System**

AutoDeskCleaner is a Python-based automation tool that automatically organizes files on your desktop by categorizing them into appropriate folders based on file type. Say goodbye to desktop clutter!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [Web Interface](#web-interface)
- [Configuration](#configuration)
- [Scheduling](#scheduling)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Automatic File Scanning**: Scans desktop directory and identifies all files
- **Smart Categorization**: Organizes files by type (Documents, Images, Videos, Audio, Archives, Code)
- **Duplicate Handling**: Automatically renames duplicate files with timestamps
- **Error Resilience**: Continues processing even if individual files fail
- **Comprehensive Logging**: Tracks all operations with detailed logs
- **Web Interface**: Modern, responsive UI for easy management
- **CLI Support**: Command-line interface for automation and scripting
- **Customizable Rules**: JSON-based configuration for personalized organization
- **Real-time Statistics**: Visual dashboard showing file distribution
- **Safe Operations**: Excludes system files and hidden files automatically

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AutoDeskCleaner                         │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                   │
│  │ ConfigManager│─────▶│   Scanner    │                   │
│  └──────────────┘      └──────┬───────┘                   │
│         │                      │                            │
│         │                      ▼                            │
│         │              ┌──────────────┐                    │
│         └─────────────▶│ Categorizer  │                    │
│                        └──────┬───────┘                    │
│                               │                             │
│                               ▼                             │
│                        ┌──────────────┐                    │
│                        │    Mover     │                    │
│                        └──────┬───────┘                    │
│                               │                             │
│                               ▼                             │
│                        ┌──────────────┐                    │
│                        │    Logger    │                    │
│                        └──────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### Components

- **ConfigManager**: Loads and manages configuration settings
- **Scanner**: Scans desktop and filters files
- **Categorizer**: Matches file extensions to categories
- **Mover**: Handles file movement with duplicate detection
- **Logger**: Tracks operations and generates reports
- **Flask API**: RESTful API for web interface
- **Frontend**: Modern web UI with real-time updates

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AutoDeskCleaner.git
cd AutoDeskCleaner
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Verify installation**
```bash
python cleaner.py --help
```

## 🚀 Usage

### CLI Mode

Run the cleaner from command line:

```bash
# Basic usage
python cleaner.py

# Dry run (preview without moving files)
python cleaner.py --dry-run

# Custom configuration file
python cleaner.py --config my_config.json
```

**Example Output:**
```
============================================================
AutoDeskCleaner - Desktop File Organizer
============================================================

Loading configuration from config.json...
Desktop path: C:\Users\YourName\Desktop
Target path: C:\Users\YourName\Desktop\Organized

Scanning desktop...
Found 45 files to process

Processing files...
  ✓ [Documents] report.pdf
  ✓ [Images] photo.jpg
  ✓ [Videos] video.mp4
  ...

============================================================
CLEANUP SUMMARY
============================================================
Total files processed: 45
Successfully moved: 43
Skipped: 0
Failed: 2

Files by category:
  Documents: 20
  Images: 15
  Videos: 5
  Others: 3
============================================================
```

### Web Interface

1. **Start the Flask server**
```bash
python src/api/app.py
```

2. **Open your browser**
```
http://localhost:5000
```

3. **Use the interface**
   - Click "Scan Desktop" to see all files
   - Review the categorization and statistics
   - Click "Clean Up Now" to organize files
   - View logs and modify configuration as needed

**Screenshots:**

![Dashboard](screenshots/dashboard.png)
*Main dashboard showing file statistics*

![File Preview](screenshots/files.png)
*File preview grouped by category*

![Configuration](screenshots/config.png)
*Configuration editor*

## ⚙️ Configuration

Edit `config.json` to customize behavior:

```json
{
  "desktop_path": "~/Desktop",
  "target_base_path": "~/Desktop/Organized",
  "categories": {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".java", ".cpp", ".html", ".css"]
  },
  "system_files": ["desktop.ini", ".DS_Store", "thumbs.db"],
  "log_file": "~/Desktop/Organized/cleanup_log.txt"
}
```

### Configuration Options

- **desktop_path**: Source directory to scan (default: ~/Desktop)
- **target_base_path**: Base directory for organized files
- **categories**: File extension mappings for each category
- **system_files**: Files to exclude from processing
- **log_file**: Path to operation log file

## ⏰ Scheduling

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily at 9:00 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `C:\path\to\AutoDeskCleaner\cleaner.py`
7. Start in: `C:\path\to\AutoDeskCleaner`

### Linux/Mac (cron)

1. Open crontab:
```bash
crontab -e
```

2. Add schedule (daily at 9 AM):
```bash
0 9 * * * cd /path/to/AutoDeskCleaner && python cleaner.py
```

3. Save and exit

## 📡 API Documentation

### Endpoints

#### `GET /api/scan`
Scan desktop and return file list with categories.

**Response:**
```json
{
  "success": true,
  "files": [...],
  "total": 45,
  "categories": {"Documents": 20, "Images": 15, ...}
}
```

#### `POST /api/cleanup`
Execute cleanup operation.

**Request:**
```json
{
  "files": [...]
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "summary": {"total_files": 45, "moved": 43, ...}
}
```

#### `GET /api/config`
Get current configuration.

#### `POST /api/config`
Update configuration.

#### `GET /api/logs`
Get recent operation logs.

## 📁 Project Structure

```
AutoDeskCleaner/
├── src/
│   ├── backend/
│   │   ├── config_manager.py    # Configuration management
│   │   ├── scanner.py            # Desktop scanning
│   │   ├── categorizer.py        # File categorization
│   │   ├── mover.py              # File movement
│   │   └── logger.py             # Operation logging
│   ├── api/
│   │   └── app.py                # Flask REST API
│   └── frontend/
│       ├── index.html            # Web interface
│       ├── main.js               # Frontend logic
│       └── styles.css            # Styling
├── cleaner.py                    # CLI entry point
├── config.json                   # Configuration file
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

## 🔧 Troubleshooting

### Common Issues

**Issue: Permission denied errors**
- Solution: Run with administrator/sudo privileges or check file permissions

**Issue: Files not moving**
- Solution: Check if files are locked by other applications
- Try closing applications that might be using the files

**Issue: Configuration not loading**
- Solution: Verify JSON syntax in config.json
- Use a JSON validator online

**Issue: Web interface not loading**
- Solution: Ensure Flask is running on port 5000
- Check if another application is using the port

**Issue: Desktop path not found**
- Solution: Update desktop_path in config.json to match your system

## 🚀 Future Enhancements

- [ ] Machine Learning-based categorization
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Mobile app for remote management
- [ ] Undo functionality for recent operations
- [ ] Custom category creation via UI
- [ ] File preview before cleanup
- [ ] Multi-language support
- [ ] Dark mode theme
- [ ] Scheduled cleanup from web interface
- [ ] Email notifications for cleanup reports

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Project: [AutoDeskCleaner](https://github.com/yourusername/AutoDeskCleaner)

## 🙏 Acknowledgments

- Built as part of AI for Bharat Week-2 Project
- Developed with assistance from AI tools (Kiro/LLM)
- Inspired by the need for automated desktop organization

---

**Made with ❤️ and Python**
