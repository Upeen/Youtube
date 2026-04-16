# 🏁 Skill: Competitive Benchmarking (Coverage Race)

## Overview
Instructions for using and maintaining the competitive "Coverage Race" feature which tracks editorial latency between channels in real-time.

## 🛠️ Implementation Details
- **Logic Module**: `app.py` (Coverage Race tab logic).
- **Primary KPI**: Editorial "Gap" (minutes/hours late relative to the fastest publisher).
- **UI Indicators**:
    - 🚀 **First Responder**: The channel that broke the story first is marked with a rocket icon.
    - 🔴 **Latency Tag**: Subsequent channels are tagged with their delay (e.g., `+12 min late` or `+1.5 hrs late`).

## 💡 Easy Understanding: Coverage Race Scenario

**Topic**: "Budget 2024"

- **Zee News**: Publishes at **11:00 AM**.
- **Aaj Tak**: Publishes at **11:15 AM**.
- **NDTV**: Publishes at **11:45 AM**.

**Dashboard Result**:
1.  **Zee News**: Marked with 🚀 **First!**
2.  **Aaj Tak**: Marked with 🔴 **+15 min late**.
3.  **NDTV**: Marked with 🔴 **+45 min late**.

*Conclusion for Editorial Team*: We need to investigate why Zee News was 15 minutes ahead of us and what sources they used.

---

## 🚀 Execution Instructions

### Using the Coverage Race
1. Enter a specific search query (e.g., "RBI Rate Cut").
2. The system filters all videos in the current cache matching the keywords within the selected **Date Range**.
3. It identifies the absolute earliest `published_at` timestamp in the matched set.
4. It calculates the temporal offset for every other channel and renders them in chronological order.

### Enhancing Keyword Matching
- The logic uses a set-based token match. To make it broader, modify the `query_tokens` logic in `app.py` to include partial matching or fuzzy string comparison.

## 🔍 Validation
- Test with a known trending topic.
- Verify that clicking "Watch on YouTube" on the winner's card opens the correct breaking news clip.
- Ensure that if only one channel covers a topic, it correctly shows "Only one coverage found" rather than a gap.
