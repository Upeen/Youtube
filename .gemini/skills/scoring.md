# 🧮 Skill: Algorithmic Scoring & TF-IDF Logic

## Overview
This skill documents the mathematics behind the recommendation engine and trend scoring. Use this to tune how content is prioritized across the Trending, Search, and Recommendation modules.

## 🛠️ Implementation Details
- **Core Engine**: `recommender.py`
- **Engagement Quality (Log-Normal)**:
    - Normalizes raw metrics to a 0-1 range to handle high-variance YouTube data.
    - `EngScore = min(1.0, (Log(Views)/8 * 0.4) + (Log(Likes)/6 * 0.35) + (Log(Comments)/5 * 0.25))`
- **Trend Velocity Algorithm**:
    - `Trend Score = (Log10(VPH + 1) / 5) * 0.6 + (EngScore * 0.4)`
- **Semantic Matching (TF-IDF)**:
    - **Title Weight**: 3x replication (Primary driver).
    - **Tags Weight**: 2x replication (Secondary driver).
    - **Description Weight**: 1x (Context provider).
- **Match Score**: Cosine Similarity calculation between query and pre-vectorized video documents.

## 🚀 Execution Instructions

### Tuning the "Sensitivity"
- To make the dashboard "Flashier" (rewarding spikes), increase the 0.6 weight of Velocity in `recommender.py`.
- To make it "higher quality" (rewarding audience loyalty), increase the 0.4 weight of `EngScore`.

### Updating the Stopword list
- If the search results contain too many generic terms (e.g. "hindi", "news"), add them to the `STOP_WORDS` set in `recommender.py` to improve similarity relevance.

## 💡 Easy Understanding: Search Match Walkthrough

**Task**: You search for **"Modi Interview"**.

1.  **Video A**: Has "Modi Interview" in the **Title**.
    - Since Title Weight = **3x**, its similarity score jumps to **0.95**.
2.  **Video B**: Has "Modi Interview" only in the **Description**.
    - Since Description Weight = **1x**, its similarity score is much lower, around **0.30**.
3.  **Video C**: Has "Modi" in Title and "Interview" in **Tags** (2x).
    - Its score lands in the middle, around **0.70**.

**Final Result**: Video A appears at the top, followed by Video C, then Video B. This ensures users find the most relevant coverage first.

---

## ⚠️ Safety & Constraints
- **Zero View Handle**: The system uses `+1` in logs to avoid `math domain error` on new videos with 0 views/likes.
- **Normalization Capping**: The `min(1.0, ...)` constraint is critical to prevent a single extreme outlier from occupying the entire top 50 list.

## 🔍 Validation
- Perform a search for a known keyword and ensure the `search_score %` displayed on the result cards aligns with content relevance.
- Ensure the **Trending Score** in the Raw Data view is between 0.0 and 1.0.
