# 🔄 Skill: Fetching and Synchronizing YouTube Data

## Overview
This skill contains the instructions for maintaining the high-performance data extraction pipeline. It utilizes parallel threading to synchronize local video metadata with the YouTube Data API v3.

## 🛠️ Implementation Details
- **Primary Script**: `fetch_data.py`
- **Concurrency Model**: `ThreadPoolExecutor` with a default of 12 concurrent workers (`CONCURRENT_THREADS`).
- **Intelligence Layer**:
    - **🔴 Live**: Defined by `liveBroadcastContent == "live"` or titles containing "LIVE" or duration $> 3600s$.
    - **🟣 Short**: Defined by `duration <= 60s` or presence of the `"shorts"` tag.
    - **⚪ Video**: Any standard long-form VOD.
- **Output Protocols**: Simultaneous saving to `data/videos.json` (for the engine) and `data/videos.csv` (for external audit).

## 🚀 Execution Instructions
To perform a full data synchronization, use the following command:
```powershell
python fetch_data.py
```

### Advanced Optimization
- **Deduplication**: The script checks `published_at` against `PUBLISHED_AFTER` (configured in `config.py`) to avoid redundant API calls for older data.
- **Auto-Resolution**: If a Channel ID fails, the script attempts a search-based fallback to find the new ID automatically.

## ⚠️ Safety & Constraints
- **Quota Management**: Each manual fetch consumes ~100-500 API units depending on the number of channels. Monitor your Google Cloud Console.
- **State Blocking**: Do not run the fetcher while manually editing the `config.py` channel list to avoid race conditions.

## 💡 Easy Understanding: Operational Walkthrough

**Task**: You want to update data for **Zee News**.

1.  **Run the script**: `python fetch_data.py`.
2.  **Pipeline starts**: It initiates 12 parallel threads.
3.  **Zee News Scanned**:
    - **Video A (55s)**: Classified as **Short** 🟣.
    - **Video B (Live Stream)**: Classified as **Live** 🔴.
    - **Video C (10m)**: Classified as **Video** ⚪.
4.  **Save Output**: All three are saved into `data/videos.json`.
5.  **Dashboard Refresh**: When you visit the site, you see the new "Zee News" entries with their respective icons under the "Trending" tab.

---

## 🔍 Validation
- Check the console output for `[OK]` status across all 11+ channels.
- Verify that the `video_type` field is correctly populated in the `Raw Data` tab of the dashboard.
