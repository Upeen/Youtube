# 🏗️ Skill: Project Architecture Mastery

## Overview
This skill encapsulates the structural knowledge of the YouTube Recommendation System. It serves as the master blueprint for understanding how high-frequency data, analytical engines, and secure UI components interact.

## 🧱 Core Pillars
1.  **Secure UI Layer (`app.py`)**:
    - **Authentication**: Restricted access via `private_key.json` upload.
    - **Architecture**: Multi-tab interface with **Localized Filters** using Streamlit `session_state` and unique widget keys.
    - **Framework**: Streamlit with custom CSS3 Glassmorphism and specialized high-contrast "True Black" theme.
2.  **High-Performance Fetcher (`fetch_data.py`)**:
    - **Concurrency**: Parallel channel scanning via `ThreadPoolExecutor`.
    - **Logic**: Intelligent classification of Shorts, Live, and Video types based on metadata duration and tags.
3.  **Analytical Engine (`recommender.py`)**:
    - **Mathematics**: Pure Python implementation of TF-IDF and Cosine Similarity (Scipy-free).
    - **Scoting**: Proprietary log-normalized ranking algorithm that merges velocity momentum with engagement quality.

## 💡 Easy Understanding: Data Lifecycle Walkthrough

1.  **Ingestion**: `fetch_data.py` pulls a video record from YouTube API.
2.  **Validation**: It classifies it as a "Short" 🟣 because it's only 45 seconds long.
3.  **Storage**: The record is written into `data/videos.json`.
4.  **Inference**: `recommender.py` scans the JSON, calculates it has high VPH, and assigns a high **Trend Score**.
5.  **Presentation**: `app.py` renders this video at #1 in the **Dashboard** Trending grid with a pulsing red badge.

---

## 📂 File System Intelligence
- `/data`: Persistent storage for `videos.json` (structured) and `videos.csv` (flat).
- `config.py`: Primary control for `CHANNEL_IDS`, `YOUTUBE_API_KEY`, and lookback `DAYS_BACK`.
- `private_key.json`: Restricted access tokens (Do not commit to version control).
- `.gemini/skills`: Strategic handoff files for autonomous agent task management.

## 🔍 Validation
- Ensure that updating `CHANNEL_IDS` in `config.py` correctly populates the **Raw Data** tab after a refresh.
- Verify that the **Coverage Race** logic in `app.py` correctly handles the chronological sorting of multiple video hits.
