# Graph Report - C:\Users\upender.sharma\OneDrive - Zee Media Corporation Limited\Desktop\Demo projects\Youtube  (2026-04-23)

## Corpus Check
- 4 files · ~16,522 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 58 nodes · 82 edges · 12 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]

## God Nodes (most connected - your core abstractions)
1. `RecommendationEngine` - 15 edges
2. `YoutubeApi` - 5 edges
3. `fetch_channel_videos()` - 5 edges
4. `load_engine()` - 4 edges
5. `initialize()` - 4 edges
6. `format_number()` - 3 edges
7. `render_video_card()` - 3 edges
8. `parse_duration()` - 3 edges
9. `format_duration()` - 3 edges
10. `fetch_all_channels()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `load_engine()` --calls--> `RecommendationEngine`  [INFERRED]
  C:\Users\upender.sharma\OneDrive - Zee Media Corporation Limited\Desktop\Demo projects\Youtube\app.py → C:\Users\upender.sharma\OneDrive - Zee Media Corporation Limited\Desktop\Demo projects\Youtube\recommender.py
- `cached_fetch_data()` --calls--> `fetch_all_channels()`  [INFERRED]
  C:\Users\upender.sharma\OneDrive - Zee Media Corporation Limited\Desktop\Demo projects\Youtube\app.py → C:\Users\upender.sharma\OneDrive - Zee Media Corporation Limited\Desktop\Demo projects\Youtube\fetch_data.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.27
Nodes (4): format_number(), render_channel_card(), render_video_card(), time_ago()

### Community 1 - "Community 1"
Cohesion: 0.24
Nodes (9): cached_fetch_data(), fetch_all_channels(), fetch_channel_videos(), format_duration(), parse_duration(), Fetch recent videos from a YouTube channel with optimization., Fetch videos from all configured channels in parallel., Convert ISO 8601 duration (PT1H2M3S) to seconds. (+1 more)

### Community 2 - "Community 2"
Cohesion: 0.47
Nodes (2): Execute a request with automatic key rotation and thread-safe service management, YoutubeApi

### Community 3 - "Community 3"
Cohesion: 0.4
Nodes (3): Get aggregated stats per channel., Content-based video recommendation engine., RecommendationEngine

### Community 4 - "Community 4"
Cohesion: 0.4
Nodes (3): get_cached_trending(), Calculate engagement score (0-1) based on views, likes, comments., Get trending videos using original Velocity + Engagement logic.

### Community 5 - "Community 5"
Cohesion: 0.4
Nodes (3): get_cached_search(), Search videos by text query using TF-IDF similarity with filters., Simple tokenizer: lowercase, remove special chars, split.

### Community 6 - "Community 6"
Cohesion: 0.5
Nodes (2): Calculate freshness score (0-1), newer = higher., Get video recommendations based on content similarity + engagement.

### Community 7 - "Community 7"
Cohesion: 0.5
Nodes (2): Build a text document from video metadata., Build TF-IDF vectors for all videos.

### Community 8 - "Community 8"
Cohesion: 0.67
Nodes (2): initialize(), Initialize the recommendation engine.

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (2): load_engine(), Load video data from JSON file.

### Community 10 - "Community 10"
Cohesion: 1.0
Nodes (1): Compute cosine similarity between two sparse vectors.

### Community 11 - "Community 11"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **18 isolated node(s):** `Execute a request with automatic key rotation and thread-safe service management`, `Convert ISO 8601 duration (PT1H2M3S) to seconds.`, `Format seconds to human readable duration.`, `Fetch recent videos from a YouTube channel with optimization.`, `Fetch videos from all configured channels in parallel.` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 10`** (2 nodes): `Compute cosine similarity between two sparse vectors.`, `._cosine_similarity()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 11`** (1 nodes): `config.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `cached_fetch_data()` connect `Community 1` to `Community 0`?**
  _High betweenness centrality (0.385) - this node is a cross-community bridge._
- **Why does `load_engine()` connect `Community 9` to `Community 0`, `Community 3`, `Community 7`?**
  _High betweenness centrality (0.356) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `load_engine()` (e.g. with `RecommendationEngine` and `.load_data()`) actually correct?**
  _`load_engine()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Execute a request with automatic key rotation and thread-safe service management`, `Convert ISO 8601 duration (PT1H2M3S) to seconds.`, `Format seconds to human readable duration.` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._