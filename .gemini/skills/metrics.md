# 📊 YT Recommender: Metrics & Scoring Documentation

This document provides a comprehensive breakdown of the analytical metrics used in the YouTube Recommendation System to rank and identify trending content.

---

## 1. Velocity (VPH)
**Description:** Measures the speed at which a video is gaining views. It is the most critical metric for identifying "breaking news."

*   **Formula:** `Total Views / Age of Video (in hours)`
*   **Logic**: The denominator is capped at `max(1, AgeHours)` in `fetch_data.py` to prevent extreme spikes in the first few minutes of publication.
*   **Example**:
    - **Video A**: 10,000 views, 1 hour old → **10,000 VPH** (Viral candidate)
    - **Video B**: 100,000 views, 100 hours old → **1,000 VPH** (Steady archive)

---

## 2. Engagement Rate (%)
**Description:** Measures the raw percentage of interaction (Likes + Comments) relative to Views.

*   **Formula:** `((Likes + Comments) / Views) * 100`
*   **Example**:
    - **Views**: 1,000 | **Likes**: 90 | **Comments**: 10
    - **Calculation**: `((90 + 10) / 1000) * 100 = 10.0%` (High quality interaction)

---

## 3. Engagement Score (Log-Normalized)
**Description:** A proprietary score between 0 and 1 that uses logarithmic scaling to normalize interaction intensity.

*   **Formula**:
    - `view_score = log10(views + 1) / 8`
    - `like_score = log10(likes + 1) / 6`
    - `comment_score = log10(comments + 1) / 5`
    - **Final Score**: `min(1.0, (view_score*0.4 + like_score*0.35 + comment_score*0.25))`
*   **Example**:
    - A video with **1,000 views** and **100 likes** might get a score of **0.25**.
    - A video with **1M views** and **50k likes** hits closer to **0.65**.

---

## 4. Freshness Score
**Description:** Rewards newer content to ensure the dashboard remains real-time.

*   **Formula (Stepped Decay):** 
    - `< 6 hrs`: 1.0
    - `< 24 hrs`: 0.9
    - `< 72 hrs`: 0.7
*   **Example**:
    - **Published 2 hours ago**: Score = **1.0** (Top priority)
    - **Published 5 days ago**: Score = **0.3** (Low priority)

---

## 5. Trend Score (The Master Metric)
**Description:** The primary sorting logic for the "Trending" tab. It balances raw momentum (Velocity) with normalized quality (Engagement).

*   **Formula:** `(log10(Velocity + 1) / 5) * 0.6 + (Engagement Score) * 0.4`
*   **Example**:
    - **High Velocity (10k VPH)** + **Low Engagement (0.2)** → Score ≈ **0.56**
    - **Medium Velocity (2k VPH)** + **High Engagement (0.8)** → Score ≈ **0.72** (Winner)

---

## 6. Coverage Gap (Race Performance)
**Description:** Measures the competitive "Time To Market."

*   **Formula:** `Target Video Published Time - First Video Published Time (for same topic)`
*   **Example**:
    - **Channel A**: Publishes at 12:00
    - **Channel B**: Publishes at 12:45
    - **Gap**: Channel B is **+45 min late**.
*   **Example**: If "Channel A" publishes at 12:00 and "Channel B" at 12:15, Channel B has a `+15 min` latency.

---

## Summary of Feature Weights
| Use Case | Formula / Primary Driver | Feature Split |
| :--- | :--- | :--- |
| **Trending Tab** | Trend Score | 60% Vel / 40% Eng |
| **Search Tab** | TF-IDF + Similarity | Title(3x), Tags(2x), Desc(1x) |
| **Recommendations** | Hybrid Sim | 50% Content / 30% Eng / 20% Fresh |
| **Dashboard** | General Rank | 60% Eng / 40% Fresh |

---

## 💡 Easy Understanding: Step-by-Step Walkthrough

Let's calculate the **Trend Score** for a hypothetical video to see how the logic works:

**Video Data:**
- **Views**: 100,000
- **Likes**: 5,000
- **Comments**: 500
- **Age**: 10 Hours

### Step 1: Calculate Velocity (VPH)
$VPH = 100,000 / 10 = \mathbf{10,000}$

### Step 2: Calculate Engagement Components (Log-Normal)
- **View Score**: $log10(100,000+1)/8 = 5/8 = \mathbf{0.625}$
- **Like Score**: $log10(5,000+1)/6 \approx 3.7/6 = \mathbf{0.616}$
- **Comment Score**: $log10(500+1)/5 \approx 2.7/5 = \mathbf{0.54}$

### Step 3: Calculate Final Engagement Score
$EngScore = (0.625 \times 0.4) + (0.616 \times 0.35) + (0.54 \times 0.25) \approx 0.25 + 0.215 + 0.135 = \mathbf{0.60}$

### Step 4: Calculate Final Trend Score
$TrendScore = (log10(10,000+1)/5 \times 0.6) + (0.60 \times 0.4)$
$TrendScore = (4/5 \times 0.6) + 0.24 = 0.48 + 0.24 = \mathbf{0.72}$

**Result**: This video is a "Strong Trend" candidate.

---

## ⚔️ Real-World Scenario: The "News Battle"
To understand how these metrics work together, consider three channels covering the same "Breaking News" event:

| Metric | 📺 Channel A | 📺 Channel B | 📺 Channel C |
| :--- | :--- | :--- | :--- |
| **Published at** | 10:00 AM (First) | 10:30 AM | 11:00 AM |
| **Current Views** | 50,000 | 45,000 | 10,000 |
| **Age** | 2 Hours | 1.5 Hours | 1 Hour |
| **Velocity (VPH)** | **25,000** | **30,000** | **10,000** |
| **Coverage Gap** | **Winner (0m)** | **Late (30m)** | **Late (60m)** |

### 🏆 The Result:
1.  **Channel B** wins the **Trending** rank because while they were 30 mins late, their **Velocity** (30k VPH) and **Engagement** are significantly higher.
2.  **Channel A** wins the **Coverage Race** for being first on the scene, but might fall in rankings if audience interaction is low.
3.  **Channel C** appears in **Search Results** but doesn't hit the Top Trends due to lower raw volume.
