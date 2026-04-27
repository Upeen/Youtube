# ============================================================
# YouTube Recommendation System - Configuration
# ============================================================

import os
from datetime import datetime, timedelta

# List of YouTube API keys for rotation (prevents quota limits)
YOUTUBE_API_KEYS = ["AIzaSyCWWBSwovSVsLZNOFKCKJt6sIC1SkhF8LQ"]

# Legacy compatibility (first key)
YOUTUBE_API_KEY = YOUTUBE_API_KEYS[0]

CHANNEL_IDS = {
    "techulsive": {"id": "UCW2s_zlmBQ0l848Y6wmOiag", "tag": "Tech"},
    "india_com": {"id": "UC8eEZ-l5z_zzG8GT0Tu0PaA", "tag": "News"},
    "cricket_country": {"id": "UCBynf-PeQTgIAyKFLvJFwoA", "tag": "sports"},
    "dna_india": {"id": "UCIRAYFbJmrP--jyrC9MAIWQ", "tag": "News"},
    "pinkvilla": {"id": "UCkJZQddO3XTCdcLjN019FjA", "tag": "Bollywood"},
    "filmibeat": {"id": "UCsaoYBUHz_lVB_dOmFwA9Zw", "tag": "Bollywood"},
    "zoom": {"id": "UCotI-SqRXnkAZX4bMqlRNjw", "tag": "Bollywood"},
    "Bollywood Life": {"id": "UC2GwMhJ9ffCY5hR_-cIz1Bw", "tag": "Bollywood"},
    "TheHealthSite": {"id": "UCOqnb0JhnoEdSjvzb5aFfFw", "tag": "Health"},
    "koimoi": {"id": "UC-Yzz2q5vFkCxbUiqJQzcEQ", "tag": "Bollywood"}
}



# ============================================================
# TIME SETTINGS: Control how far back to fetch data
# ============================================================
# HOURS_BACK controls how far back to fetch data (e.g., 24 for last 24 hours)
HOURS_BACK =96

# ============================================================

# ============================================================
# Data storage path
# ============================================================
DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

VIDEO_DATA_FILE = os.path.join(DATA_DIR, "videos.json")
RECOMMENDATIONS_FILE = os.path.join(DATA_DIR, "recommendations.json")