# 🧮 Skill: Algorithmic Scoring & TF-IDF Logic

## Overview
This skill documents the mathematics behind the recommendation engine and trend scoring. Use this to tune how content is prioritized.

## 🛠️ Implementation Details
- **Recommendation Logic**: `recommender.py`
- **Scoring Formulas**: 
  - **Trend Score**: `(NormalizedVPH * 0.6) + (EngScore * 0.4)`
  - **Match Score**: TF-IDF Cosine Similarity.
  - **Engagement Score**: Log-scaled metrics of (Views, Likes, Comments).

## 🚀 Execution Instructions

### Tuning Feature Weights
- Adjust the `FEATURE_WEIGHTS` dictionary in `recommender.py` to change the importance of Title vs. Tags vs. Description.
- Modify the scoring multipliers in the `calculate_scores` function to prioritize freshness over engagement (or vice versa).

### Adding New Metrics
1. Extract the metric in `fetch_data.py`.
2. Update the `preprocess_data` function in `recommender.py` to include the new field.
3. Incorporate it into the final weight aggregation.

## ⚠️ Safety & Constraints
- **Normalization**: Always log-normalize high-variance metrics like view counts to prevent viral outliers from breaking the distribution.
- **TF-IDF Sparsity**: Ensure clean text normalization before vectorization to avoid noisy features.

## 🔍 Validation
- Use the **Search** tab to verify if the ranking of results feels "smarter" after tuning.
- Check the **Trending** tab to ensure the top 5 videos have a high views-per-hour (VPH) ratio.
