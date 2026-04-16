# ⚙️ Skill: Configuration & Channel Management

## Overview
This skill defines how to manage the system's global settings, including API keys, tracked channels, and search parameters.

## 🛠️ Implementation Details
- **Configuration File**: `config.py`
- **Tracked Network**: `CHANNEL_IDS` (dictionary of 11+ major news networks).
- **Time Window**: `DAYS_BACK` integer (Controls the lookback depth).
- **API Target**: `PUBLISHED_AFTER` is automatically calculated as an ISO timestamp based on `DAYS_BACK`.

## 💡 Easy Understanding: Configuration Walkthrough

**Task**: You want to track a new competitor, **Local News**.

1.  **Find ID**: You find their YouTube ID: `UC_LOCAL_NEWS_123`.
2.  **Edit `config.py`**:
    ```python
    CHANNEL_IDS = {
        ...,
        "local_news": "UC_LOCAL_NEWS_123"
    }
    ```
3.  **Adjust Depth**: You want to see their last 5 days of history.
    - Set `DAYS_BACK = 5`.
4.  **Fetch**: The next time you click "Fetch" in the UI, the system will pull 5 days of data for strictly these 12 channels.

---

## 🚀 Execution Instructions

### Adding a New Channel
1. Obtain the YouTube Channel ID (e.g., `UC...` or `@handle`).
2. Add a new entry to the `CHANNEL_IDS` dictionary in `config.py`.
3. Restart the Streamlit dashboard and click **"Fetch Fresh Data"** to trigger a sync for the new channel.

### Updating API Keys
- Replace the `YOUTUBE_API_KEY` string. Ensure the key has the "YouTube Data API v3" enabled in the Google Cloud Console.

### Adjusting Data Depth
- Change `DAYS_BACK = 2` to `DAYS_BACK = 7` to pull a week's worth of data.
- **Note**: Increasing this significantly will increase the time taken for the "Fetch" operation.

## ⚠️ Safety & Constraints
- **Key Security**: Current implementation uses a hardcoded key in `config.py` for ease of use in local demis, but should be moved to environment variables for production.
- **Deduplication**: The `fetch_data.py` logic automatically handles duplicate entries if the API returns the same video multiple times.

## 🔍 Validation
- Change `DAYS_BACK` to `1` and run the fetcher.
- Verify in the **Raw Data** explorer that no videos older than 24 hours are present.
