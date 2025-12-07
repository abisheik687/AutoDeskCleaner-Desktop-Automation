# AutoDeskCleaner Design Document

## Overview

AutoDeskCleaner is a modular Python application that automates desktop file organization through a pipeline architecture. The system consists of five core components: Scanner, Categorizer, Mover, Logger, and ConfigManager. The application follows a single-pass processing model where files are scanned once, categorized based on configurable rules, and moved to appropriate destination folders with comprehensive logging.

The design prioritizes simplicity, modularity, and error resilience. Each component has a single responsibility and can be tested independently. The system uses JSON for configuration to enable easy customization without code changes.

## Architecture

### High-Level Architecture

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

### Component Responsibilities

**ConfigManager**: Loads and validates configuration from JSON file, provides default configuration if file is missing, exposes category mappings and settings to other components.

**Scanner**: Traverses the desktop directory, identifies files (excluding directories, hidden files, and system files), extracts file extensions, returns list of file paths for processing.

**Categorizer**: Receives file paths from Scanner, matches file extensions against configuration rules, assigns category to each file, handles uncategorized files with default "Others" category.

**Mover**: Creates target directories as needed, handles duplicate files by appending timestamps, moves files from desktop to categorized folders, manages file operation errors gracefully.

**Logger**: Records all operations with timestamps, tracks success and failure states, writes to persistent log file, generates execution summary statistics.

### Data Flow

```
1. User executes cleaner.py
2. ConfigManager loads config.json
3. Scanner identifies files on desktop
4. For each file:
   a. Categorizer determines target category
   b. Mover creates target folder if needed
   c. Mover checks for duplicates
   d. Mover transfers file
   e. Logger records operation
5. Logger displays summary
6. Logger writes to log file
```

## Components and Interfaces

### ConfigManager

```python
class ConfigManager:
    def load_config(self, config_path: str) -> dict
    def get_categories(self) -> dict
    def get_desktop_path(self) -> str
    def get_target_base_path(self) -> str
    def create_default_config(self, config_path: str) -> None
```

**Responsibilities:**
- Load and parse JSON configuration
- Validate configuration structure
- Provide default configuration if missing
- Expose configuration data to other components

### Scanner

```python
class Scanner:
    def scan_desktop(self, desktop_path: str) -> list[str]
    def is_system_file(self, filename: str) -> bool
    def is_hidden_file(self, filename: str) -> bool
    def get_file_extension(self, filepath: str) -> str
```

**Responsibilities:**
- Traverse desktop directory
- Filter out directories, hidden files, system files
- Extract file extensions
- Return list of processable file paths

### Categorizer

```python
class Categorizer:
    def __init__(self, categories: dict)
    def categorize_file(self, filepath: str) -> str
    def get_category_for_extension(self, extension: str) -> str
```

**Responsibilities:**
- Match file extensions to categories
- Handle uncategorized files
- Return target category name

### Mover

```python
class Mover:
    def move_file(self, source: str, category: str, base_path: str) -> tuple[bool, str]
    def create_target_directory(self, directory_path: str) -> bool
    def handle_duplicate(self, target_path: str) -> str
    def generate_timestamp_suffix(self) -> str
```

**Responsibilities:**
- Create target directories
- Handle duplicate files with timestamp renaming
- Execute file moves
- Return operation status and destination path

### Logger

```python
class Logger:
    def log_operation(self, operation: dict) -> None
    def log_error(self, filepath: str, error: str) -> None
    def get_summary(self) -> dict
    def write_to_file(self, log_path: str) -> None
    def display_summary(self) -> None
```

**Responsibilities:**
- Record all operations with timestamps
- Track statistics (processed, moved, skipped, failed)
- Write persistent log file
- Display execution summary

## Data Models

### Configuration Structure (config.json)

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

### Operation Record

```python
{
    "timestamp": "2025-12-07 14:30:45",
    "source": "/Users/name/Desktop/document.pdf",
    "destination": "/Users/name/Desktop/Organized/Documents/document.pdf",
    "category": "Documents",
    "status": "success|failed|skipped",
    "error": "error message if failed"
}
```

### Summary Statistics

```python
{
    "total_files": 50,
    "moved": 45,
    "skipped": 3,
    "failed": 2,
    "categories": {
        "Documents": 20,
        "Images": 15,
        "Videos": 5,
        "Others": 5
    }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Scanning Properties

**Property 1: Complete file discovery**
*For any* directory containing files and subdirectories, scanning should return all files (excluding subdirectories) in that directory.
**Validates: Requirements 1.1, 1.3**

**Property 2: Extension extraction accuracy**
*For any* file with a valid filename, extracting the extension should return the correct suffix after the last dot, or empty string if no extension exists.
**Validates: Requirements 1.2**

**Property 3: System file exclusion**
*For any* file list containing system files (desktop.ini, .DS_Store, thumbs.db), scanning should exclude all system files from the results.
**Validates: Requirements 1.4**

**Property 4: Hidden file exclusion**
*For any* file whose name begins with a dot, scanning should exclude that file from the results.
**Validates: Requirements 1.5**

### Categorization Properties

**Property 5: Extension matching correctness**
*For any* file extension that exists in the configuration categories, categorization should assign the file to the correct category.
**Validates: Requirements 2.1, 2.2**

**Property 6: Default category assignment**
*For any* file extension that does not exist in any configuration category, categorization should assign the file to the "Others" category.
**Validates: Requirements 2.3**

**Property 7: Category grouping consistency**
*For any* set of files with extensions mapped to the same category, all files should receive the same category assignment.
**Validates: Requirements 2.4**

### File Movement Properties

**Property 8: Target directory creation**
*For any* category that does not have an existing target directory, the system should create that directory before moving files.
**Validates: Requirements 3.1**

**Property 9: File transfer completeness**
*For any* file successfully moved, the file should exist at the destination path and not exist at the source path.
**Validates: Requirements 3.2**

**Property 10: Duplicate handling with timestamps**
*For any* file moved to a destination where a file with the same name already exists, the new file should be renamed with a timestamp suffix before moving.
**Validates: Requirements 3.3**

**Property 11: Error resilience during processing**
*For any* batch of files where some files encounter permission errors or are locked by other processes, the system should continue processing all remaining files and log each error.
**Validates: Requirements 3.5, 6.1, 6.3**

**Property 12: Directory creation error handling**
*For any* category whose target directory cannot be created due to permissions, all files assigned to that category should be skipped with errors logged.
**Validates: Requirements 6.2**

### Configuration Properties

**Property 13: Configuration loading correctness**
*For any* valid JSON configuration file, the system should successfully load and parse all categorization rules.
**Validates: Requirements 4.1**

**Property 14: Configuration rule application**
*For any* modified configuration file, the next execution should apply the updated categorization rules to all processed files.
**Validates: Requirements 4.4**

### Logging Properties

**Property 15: Operation logging completeness**
*For any* file processed by the system, an operation record should exist in the log.
**Validates: Requirements 5.1**

**Property 16: Log entry structure completeness**
*For any* logged operation, the log entry should contain timestamp, source path, destination path, category, and status fields.
**Validates: Requirements 5.2**

**Property 17: Log persistence**
*For any* execution of the system, all operation records should be appended to the persistent log file.
**Validates: Requirements 5.3**

**Property 18: Error logging completeness**
*For any* file operation that fails, an error record should exist in the log containing the file path and error details.
**Validates: Requirements 5.4**

**Property 19: Summary statistics accuracy**
*For any* execution, the summary should display counts that equal the actual number of files processed, moved, skipped, and failed.
**Validates: Requirements 5.5**

### Execution Consistency Properties

**Property 20: Invocation consistency**
*For any* execution context (manual, scheduled, or automated), the system should process files with identical categorization and movement behavior.
**Validates: Requirements 8.3**

## Error Handling

### Error Categories

**File Access Errors:**
- Permission denied when reading source file
- Permission denied when writing to destination
- File locked by another process
- File deleted during processing

**Strategy:** Log error with file path, increment failed counter, continue processing remaining files.

**Directory Errors:**
- Cannot create target directory due to permissions
- Target path is a file instead of directory
- Disk space exhausted

**Strategy:** Log error, skip all files for affected category, continue with other categories.

**Configuration Errors:**
- Missing configuration file
- Invalid JSON syntax
- Missing required configuration fields

**Strategy:** For missing file, create default configuration. For invalid syntax or structure, display error message and terminate execution.

**System Errors:**
- Desktop path does not exist
- Cannot write to log file
- Insufficient disk space

**Strategy:** Display clear error message, log what was possible, terminate gracefully.

### Error Recovery

The system implements a fail-safe approach where individual file failures do not stop overall execution. Each file operation is wrapped in error handling that:

1. Catches the specific exception
2. Logs the error with context (file path, operation, error message)
3. Increments the appropriate failure counter
4. Continues to the next file

This ensures maximum files are processed even when some operations fail.

## Testing Strategy

### Unit Testing Approach

Unit tests will verify specific behaviors and edge cases:

**Scanner Module:**
- Empty directory returns empty list
- Directory with only subdirectories returns empty list
- Mixed files and directories returns only files
- System files are correctly identified and excluded
- Hidden files are correctly identified and excluded

**Categorizer Module:**
- Known extensions map to correct categories
- Unknown extensions map to "Others"
- Case-insensitive extension matching
- Extensions without leading dot are handled

**Mover Module:**
- Successful file move removes source file
- Duplicate detection works correctly
- Timestamp suffix format is valid
- Directory creation succeeds for new paths

**Logger Module:**
- Log entries contain all required fields
- Summary statistics match actual operations
- Log file is created if missing
- Log file is appended, not overwritten

**ConfigManager Module:**
- Valid JSON is parsed correctly
- Invalid JSON raises appropriate error
- Missing config triggers default creation
- Default config contains standard categories

### Property-Based Testing Approach

Property-based tests will verify universal properties across many randomly generated inputs using the **Hypothesis** library for Python. Each test will run a minimum of 100 iterations with varied inputs.

**Key Properties to Test:**

1. **Scanning invariants:** Any file in a directory should be discoverable by the scanner (excluding hidden/system files)
2. **Categorization determinism:** Same file extension always produces same category
3. **Move operation atomicity:** File exists at exactly one location (source or destination) after move attempt
4. **Duplicate handling uniqueness:** No two files in same directory should have identical names after duplicate resolution
5. **Error isolation:** Failure processing one file never prevents processing of other files
6. **Log completeness:** Number of log entries equals number of files processed
7. **Summary accuracy:** Sum of moved + skipped + failed equals total processed

Each property-based test will be tagged with a comment referencing the specific correctness property from this design document using the format: `# Feature: auto-desk-cleaner, Property X: [property text]`

### Testing Framework

- **Unit Testing:** Python's built-in `unittest` framework
- **Property-Based Testing:** Hypothesis library
- **Test Organization:** Tests co-located with source in `test_*.py` files
- **Coverage Goal:** Minimum 80% code coverage for core logic

### Test Execution

Tests should be executable via:
```bash
python -m unittest discover
python -m pytest  # For hypothesis tests
```

Continuous integration should run all tests on every commit to ensure correctness is maintained throughout development.
