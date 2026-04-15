# 🏗️ Skill: Project Architecture Mastery

## Overview
This skill encapsulates the structural knowledge of the YouTube Recommendation System. It is the "Master Blueprint" for understanding how the data, engine, and UI components interact.

## 🧱 Core Pillars
1.  **The Intake Pipeline (`fetch_data.py`)**:
    - **Method**: Parallel execution via `ThreadPoolExecutor`.
    - **Optimization**: Skips processed videos to minimize quota usage.
2.  **The Analytics Brain (`recommender.py`)**:
    - **Logic**: Custom hybrid scoring (not utilizing external ML libraries to maintain local speed).
    - **Search**: Scipy-free cosine similarity using standard math.
3.  **The Presentation Layer (`app.py`)**:
    - **Framework**: Streamlit with custom CSS "Glassmorphism" injection.
    - **Responsive Design**: Auto-scaling cards for different viewports.

## 📂 File System Intelligence
- `/data`: Persistent JSON storage for cached videos.
- `config.py`: Central control for API keys, lookback windows, and channel lists.
- `.gemini/skills`: The "Memory Bank" for autonomous agent handoffs.

## 🔍 Validation
- Verify that `start.sh` properly initializes the environment.
- Ensure `VIDEO_DATA_FILE` is valid JSON and not corrupted during parallel writes.
