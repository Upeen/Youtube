# ⚙️ Skill: Configuration & Channel Management

## Overview
This skill defines how to manage the system's global settings, including API keys, tracked channels, and search parameters.

## 🛠️ Implementation Details
- **Configuration File**: `config.py`
- **Primary Data Structures**: `CHANNEL_IDS` (dict), `YOUTUBE_API_KEY` (string).

## 🚀 Execution Instructions

### Adding a New Channel
1. Obtain the YouTube Channel ID (e.g., `UC...`).
2. Add a new entry to the `CHANNEL_IDS` dictionary in `config.py`:
   ```python
   CHANNEL_IDS = {
       "Channel Name": "UC_ID_HERE",
       ...
   }
   ```
3. Run `python fetch_data.py` to populate data for the new channel.

### Updating API Keys
- Replace the `YOUTUBE_API_KEY` string with a fresh key from the Google Cloud Console.

### Adjusting Time Windows
- Modify `DAYS_BACK` to control how far into the past the system looks for content.

## ⚠️ Safety & Constraints
- **Key Security**: Never commit your `config.py` with the API key to public repositories. 
- **Formatting**: Ensure channel IDs are strings and keys are comma-separated if using multiple (though current implementation uses one).

## 🔍 Validation
- Restart the Streamlit dashboard (`streamlit run app.py`).
- Use the sidebar filter to check if the new channel appears in the dropdown list.
