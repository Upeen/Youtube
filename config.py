# ============================================================
# YouTube Recommendation System - Configuration
# ============================================================

import os
from datetime import datetime, timedelta

YOUTUBE_API_KEY = "AIzaSyDSbns8dqoHCXumzfLKQo4lnacRatL0Km4"

CHANNEL_IDS = {
    "zee_news": "UCIvaYmXn910QMdemBG3v1pQ",
    "times_of_india": "UCckHqySbfy5FcPP6MD_S-Yg",
    "news18_india": "UC5C1Gx5z9rC3G2l0U0sF8cg",
    "aaj_tak": "UCt4t-jeY85JegMlZ-E5UWtA",
    "india_tv": "UCmUZnRRWq2BQ5V9xQWZpQ9g",
    "ndtv": "UCZFMm1mMw0F81Z37aaEzTUA",
    "abp_news": "UCmphdqZNmqL72WJ2uyiNw5w"
}

# ============================================================
# TIME SETTINGS: Control how far back to fetch data
# ============================================================
# Change this single variable to control the fetch duration (e.g., 5, 10, 15, 30 days)
DAYS_BACK = 2

# This automatically calculates the ISO timestamp required by the YouTube API
PUBLISHED_AFTER = (datetime.utcnow() - timedelta(days=DAYS_BACK)).isoformat("T") + "Z"

# Current cut-off date: {PUBLISHED_AFTER}
# ============================================================

# ============================================================
# Data storage path
# ============================================================
DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

VIDEO_DATA_FILE = os.path.join(DATA_DIR, "videos.json")
RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "recommendations.json")