# 🏁 Skill: Competitive Benchmarking (Coverage Race)

## Overview
Instructions for using and maintaining the competitive "Coverage Race" feature which tracks editorial latency between channels.

## 🛠️ Implementation Details
- **Logic Module**: `app.py` (Coverage Race tab processing)
- **Primary KPI**: Editorial "Gap" (minutes late relative to the first reporter).

## 🚀 Execution Instructions

### Using the Coverage Race
1. Enter a specific search query (e.g., "RBI Policy").
2. The system filters videos containing this keyword.
3. It identifies the earliest `publishedAt` timestamp.
4. It calculates the offset for all other channels that covered the same topic.

### Enhancing Keyword Matching
- Modify the `fuzzy_search` or manual keyword filter logic in the Coverage Race tab section of `app.py` to allow for broader matches.

## 🔍 Validation
- Test with a known "Breaking News" topic.
- Ensure the channel that published first is marked with the 🚀 icon.
- Verify that time gaps (e.g., "+45 min") accurately reflect the difference in publication times.
