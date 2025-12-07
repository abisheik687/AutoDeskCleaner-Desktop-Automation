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
│                        │    L