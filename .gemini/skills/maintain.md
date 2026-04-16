# 🛠️ Skill: Project Maintenance & Operational Health

## Overview
Instructions for general upkeep, dependency updates, and environment management.

## 🛠️ Implementation Details
- **Dependency Tracking**: `requirements.txt`
- **Shell Automation**: `start.sh`, `start.bat`
- **Persistence**: `data/` directory

## 🚀 Execution Instructions

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Cleaning Data Cache
- Delete the contents of the `data/` folder and run `python fetch_data.py`. This is recommended after significant configuration changes or if data corruption is suspected.

### Environment Setup
- Ensure Python 3.11+ is used for better performance with modern Streamlit features.
- In Linux/macOS, ensure `start.sh` has execution permissions (`chmod +x start.sh`).

## ⚠️ Safety & Constraints
- **File Locks**: Close the Streamlit app before performing major file system operations.
- **Git Hygiene**: Ensure `data/` files are either ignored or properly versioned if small.

## 🔍 Validation
- Run `python -m pip check` to ensure no dependency conflicts exist.
- Verify that `start.bat` successfully launches the dashboard without errors.
