# 🔄 Skill: Fetching and Synchronizing YouTube Data

## Overview
This skill contains the instructions for executing the data extraction pipeline which synchronizes the local cache with the YouTube Data API v3. 

## 🛠️ Implementation Details
- **Primary Script**: `fetch_data.py`
- **Output Files**: `data/videos.json`, `data/videos.csv`
- **Shorts Logic**: Content is tagged as "Short" if `duration <= 60s` OR the tag `"shorts"` is present in the video metadata.
- **Authentication**: The system requires a `private_key.json` file for authorization, validated against `project_id`.

## 🚀 Execution Instructions
To perform a full data synchronization, use the following command:
```powershell
python fetch_data.py
```

### Advanced Parameters
- To change the lookback period, modify `DAYS_BACK` in `config.py`.
- To increase/decrease results per channel, update `MAX_RESULTS_PER_CHANNEL` in `fetch_data.py`.

## ⚠️ Safety & Constraints
- **API Key Required**: Ensure `YOUTUBE_API_KEY` in `config.py` is valid.
- **Data Integrity**: Do not manually edit `data/videos.json` while the script is running.
- **Timeout**: Each channel fetch takes ~2-5 seconds. Total time scales with the number of channels.

## 🔍 Validation
After execution, verify that:
1. `data/videos.json` size has increased or timestamps are updated.
2. The Streamlit dashboard shows the "Last Data Refreshed" timestamp matching the execution time.
