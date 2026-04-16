# 🛠️ Skill: Project Maintenance & Operational Health

## Overview
Instructions for general upkeep, dependency updates, and environment management.

## 🛠️ Implementation Details
- **Dependency Tracking**: `requirements.txt`
- **Shell Automation**: `start.sh`, `start.bat`
- **Persistence**: `data/` directory

## 💡 Easy Understanding: Maintenance Scenario

**Problem**: The dashboard feels slow or the view counts seem "stuck" for some videos.

1.  **Stop the App**: Close the terminal running Streamlit.
2.  **Purge Cache**: Delete all files inside the `/data` folder.
3.  **Perform Clean Sync**: Run `python fetch_data.py` to rebuild the JSON from scratch.
4.  **Verify Integrity**: Check `VIDEO_DATA_FILE` size. If it's $>0$, the re-sync was successful.
5.  **Restart**: Run `./start.sh` to see the fresh, high-performance dashboard.

---

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
