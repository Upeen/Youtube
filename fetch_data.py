import os
import json
import re
import csv
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY, CHANNEL_IDS, DATA_DIR, VIDEO_DATA_FILE, PUBLISHED_AFTER

MAX_RESULTS_PER_CHANNEL = 500  # Reduced for speed, can be adjusted
CONCURRENT_THREADS = 12


def get_youtube_service():
    """Build and return YouTube API service."""
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY, cache_discovery=False)


def parse_duration(duration_str):
    """Convert ISO 8601 duration (PT1H2M3S) to seconds."""
    if not duration_str:
        return 0
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


def format_duration(seconds):
    """Format seconds to human readable duration."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}m {secs}s"
    else:
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hrs}h {mins}m"


def fetch_channel_videos(channel_id, channel_name):
    """Fetch recent videos from a YouTube channel with optimization."""
    youtube = get_youtube_service()
    videos = []

    # Handle different channel identifier formats (ID, Handle, Username)
    try:
        kwargs = {"part": "contentDetails,statistics,snippet"}
        if channel_id.startswith("@"):
            kwargs["forHandle"] = channel_id[1:]
        elif channel_id.startswith("UC"):
            kwargs["id"] = channel_id
        else:
            kwargs["forUsername"] = channel_id
            
        channel_response = youtube.channels().list(**kwargs).execute()
        
        # Fallback if standard ID fails (some channels change or get disabled)
        if not channel_response.get("items") and channel_id.startswith("UC"):
            # Try a search as last resort if ID fails
            search_resp = youtube.search().list(part="snippet", type="channel", q=channel_name, maxResults=1).execute()
            if search_resp.get("items"):
                alt_id = search_resp["items"][0]["snippet"]["channelId"]
                print(f"  [!] ID failed for {channel_name}, auto-resolved to: {alt_id}")
                channel_response = youtube.channels().list(part="contentDetails,statistics,snippet", id=alt_id).execute()
                
    except Exception as e:
        print(f"  [X] Error fetching channel info for {channel_name}: {e}")
        return []

    if not channel_response.get("items"):
        print(f"  [X] No channel found for {channel_name}")
        return []

    channel_info = channel_response["items"][0]
    uploads_playlist_id = channel_info["contentDetails"]["relatedPlaylists"]["uploads"]
    channel_thumbnail = channel_info["snippet"]["thumbnails"].get("default", {}).get("url", "")
    channel_subscribers = int(channel_info["statistics"].get("subscriberCount", 0))

    # Threshold for date filtering
    pub_after_date = datetime.fromisoformat(PUBLISHED_AFTER.replace("Z", "+00:00"))

    # 1. Fetch video IDs from uploads playlist (stop when we hit old videos)
    video_ids = []
    next_page_token = None
    fetched_count = 0
    stop_fetching = False

    while fetched_count < MAX_RESULTS_PER_CHANNEL and not stop_fetching:
        try:
            playlist_response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
        except Exception as e:
            print(f"  [X] Error fetching playlist for {channel_name}: {e}")
            break

        items = playlist_response.get("items", [])
        if not items:
            break

        for item in items:
            # Check the date from playlistItem snippet before adding
            pub_date_str = item["contentDetails"].get("videoPublishedAt")
            if pub_date_str:
                v_pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                if v_pub_date < pub_after_date:
                    stop_fetching = True
                    break
            
            video_ids.append(item["contentDetails"]["videoId"])
            fetched_count += 1
            if fetched_count >= MAX_RESULTS_PER_CHANNEL:
                stop_fetching = True
                break

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token or stop_fetching:
            break

    # 2. Fetch video details in batches of 50
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i + 50]
        try:
            video_response = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(batch_ids)
            ).execute()
        except Exception as e:
            print(f"  [X] Error fetching video details: {e}")
            continue

        for item in video_response.get("items", []):
            snippet = item["snippet"]
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})

            duration_seconds = parse_duration(content.get("duration", ""))
            views = int(stats.get("view_count", stats.get("viewCount", 0)))
            likes = int(stats.get("like_count", stats.get("likeCount", 0)))
            comments = int(stats.get("comment_count", stats.get("commentCount", 0)))
            engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0

            published_at = snippet.get("publishedAt", "")
            pub_date = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - pub_date).total_seconds() / 3600

            title = snippet.get("title", "")
            tags = [t.lower() for t in snippet.get("tags", [])]
            live_status = snippet.get("liveBroadcastContent", "none")
            
            if live_status == "live" or "LIVE" in title.upper() or duration_seconds > 3600:
                video_type = "Live"
            elif (0 < duration_seconds <= 60) or ("shorts" in tags):
                video_type = "Short"
            else:
                video_type = "Video"

            video_data = {
                "video_id": item["id"],
                "title": snippet.get("title", ""),
                "description": snippet.get("description", "")[:500],
                "channel_name": channel_name,
                "channel_id": channel_id,
                "video_type": video_type,
                "channel_thumbnail": channel_thumbnail,
                "channel_subscribers": channel_subscribers,
                "published_at": published_at,
                "date_published": published_at[:10],
                "age_hours": round(age_hours, 1),
                "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                "tags": snippet.get("tags", [])[:15],
                "category_id": snippet.get("categoryId", ""),
                "duration_seconds": duration_seconds,
                "duration_formatted": format_duration(duration_seconds),
                "view_count": views,
                "like_count": likes,
                "comment_count": comments,
                "engagement_rate": round(engagement_rate, 4),
                "url": f"https://www.youtube.com/watch?v={item['id']}",
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }
            videos.append(video_data)
    
    print(f"  [OK] {channel_name}: fetched {len(videos)} videos")
    return videos


def fetch_all_channels():
    """Fetch videos from all configured channels in parallel."""
    print("=" * 60)
    print("  🚀 Optimized YouTube Data Fetcher (Parallel)")
    print("=" * 60)

    start_time = datetime.now()
    all_videos = []

    # Use ThreadPoolExecutor for parallel fetching
    with ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        futures = {executor.submit(fetch_channel_videos, cid, name): name 
                   for name, cid in CHANNEL_IDS.items()}
        
        for future in futures:
            name = futures[future]
            try:
                results = future.result()
                all_videos.extend(results)
            except Exception as e:
                print(f"  [X] Exception for {name}: {e}")

    # Save to JSON
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(VIDEO_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "total_videos": len(all_videos),
            "channels": list(CHANNEL_IDS.keys()),
            "videos": all_videos
        }, f, ensure_ascii=False, indent=2)

    # Save to CSV
    if all_videos:
        video_csv_file = VIDEO_DATA_FILE.replace(".json", ".csv")
        keys = all_videos[0].keys()
        with open(video_csv_file, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_videos)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{'=' * 60}")
    print(f"  Total videos: {len(all_videos)}")
    print(f"  Execution time: {duration:.2f} seconds")
    print(f"  Data saved to: {VIDEO_DATA_FILE}")
    print(f"{'=' * 60}")

    return all_videos


if __name__ == "__main__":
    fetch_all_channels()
