# 📊 YT Recommender: Metrics & Scoring Documentation

This document provides a comprehensive breakdown of the analytical metrics used in the YouTube Recommendation System to rank and identify trending content.

---

## 1. Velocity (VPH)
**Description:** Measures the speed at which a video is gaining views. It is the most critical metric for identifying "breaking news."

*   **Formula:** `Total Views / Age of Video (in hours)`
*   **Use Case:** Identifying which video is currently "exploding" regardless of its total view count.
*   **Example:** 
    *   **Video A:** 10,000 views, 1 hour old → **10,000 VPH** (Breaking News)
    *   **Video B:** 100,000 views, 100 hours old → **1,000 VPH** (Steady Content)

---

## 2. Engagement Rate (%)
**Description:** Measures the quality of the audience interaction. It identifies how "sticky" or "controversial" a video is.

*   **Formula:** `((Likes + Comments) / Views) * 100`
*   **Use Case:** Filtering out videos with high views but low audience interest (potential clickbait).
*   **Example:**
    *   **Views:** 1,000 | **Likes:** 90 | **Comments:** 10
    *   **Calculation:** `((90 + 10) / 1000) * 100 = 10.0%`

---

## 3. Engagement Score (Normalized)
**Description:** A proprietary score between 0 and 1 that normalizes the Engagement Rate to prevent outliers from skewing the results.

*   **Formula:** `min(1.0, Engagement Rate / 10.0)`
*   **Use Case:** Used as a weighted component in the final **Trend Score**.
*   **Example:**
    *   An engagement rate of **5%** results in a score of **0.5**.
    *   An engagement rate of **15%** results in a score of **1.0** (Capped).

---

## 4. Freshness Score
**Description:** Penalizes older content to ensure the dashboard remains "real-time."

*   **Formula (Simplified):** 
    *   `< 6 hrs`: 1.0
    *   `< 24 hrs`: 0.9
    *   `< 72 hrs`: 0.7
    *   `> 1 month`: 0.1
*   **Use Case:** Ensuring that yesterday's top news doesn't bury today's breaking updates.
*   **Example:** A 2-hour-old video gets the maximum multiplier (1.0), while a 5-day-old video only gets 0.3.

---

## 5. Trend Score (The Master Metric)
**Description:** The primary sorting logic for the "Trending" tab. It balances raw popularity (Velocity) with audience quality (Engagement).

*   **Formula:** `(log10(Velocity + 1) / 5) * 0.6 + (Engagement Score) * 0.4`
*   **Use Case:** Automating the discovery of videos that are both viral AND highly engaging.
*   **Example:**
    *   **Velocity:** 10,000 VPH (`log10(10001) ≈ 4.0`)
    *   **Engagement Score:** 0.8
    *   **Calculation:** `(4.0 / 5 * 0.6) + (0.8 * 0.4) = 0.48 + 0.32 = 0.80 (High Trend Rank)`

---

## 6. Coverage Gap (Race Performance)
**Description:** Measures the competitive "Time To Market."

*   **Formula:** `Target Video Published Time - First Video Published Time (for same topic)`
*   **Use Case:** Identifying which channel is consistently "The First Responder" in the news cycle.
*   **Example:**
    *   **Zee News:** 12:00 PM (First)
    *   **Aaj Tak:** 12:15 PM
    *   **Gap:** Aaj Tak was **15 minutes late** to cover this story.

---

## Summary of Weights
| Module | Velocity Weight | Engagement Weight | Freshness Weight |
| :--- | :--- | :--- | :--- |
| **Trending Tab** | 60% | 40% | Applied via Filter |
| **Search Tab** | N/A (Similarity) | 30% | 20% |
| **Dashboard** | N/A | 60% | 40% |

---

## ⚔️ Real-World Scenario: The "News Battle"
To understand how these metrics work together, consider three channels covering the same "Breaking News" event:

| Metric | 📺 Zee News | 📺 Aaj Tak | 📺 NDTV |
| :--- | :--- | :--- | :--- |
| **Published at** | 10:00 AM (First) | 10:30 AM | 11:00 AM |
| **Current Views** | 50,000 | 45,000 | 10,000 |
| **Age** | 2 Hours | 1.5 Hours | 1 Hour |
| **Likes/Comments**| 500 (1%) | 4,500 (10%) | 1,000 (10%) |
| **Velocity (VPH)** | **25,000** | **30,000** | **10,000** |
| **Coverage Gap** | **Winner (0m)** | **Late (30m)** | **Late (60m)** |

### 🏆 The Result:
1. **Aaj Tak** wins the **Trending** rank because while they were 30 mins late, their **Velocity** (30k VPH) and **Engagement** (10%) are significantly higher than Zee News.
2. **Zee News** wins the **Coverage Race** but will eventually fall in the rankings because of low audience engagement (1%).
3. **NDTV** appears in the **Search Results** but doesn't hit the Top Trends yet due to lower raw view volume compared to the leaders.
