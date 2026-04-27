import os
import json
import re
import csv
import threading
import shutil
from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import YOUTUBE_API_KEYS, CHANNEL_IDS, DATA_DIR, VIDEO_DATA_FILE, HOURS_BACK

MAX_RESULTS_PER_CHANNEL = 3000  # Reduced for speed, can be adjusted
CONCURRENT_THREADS = 25

class YoutubeApi:
    def __init__(self, keys):
        self.keys = keys
        self.index_lock = threading.RLock()
        self.current_key_index = 0
        self._thread_local = threading.local()
        
    def _get_service(self):
        # Build service for current thread if needed
        if not hasattr(self._thread_local, 'service_idx') or self._thread_local.service_idx != self.current_key_index:
            with self.index_lock:
                key = self.keys[self.current_key_index]
            self._thread_local.service = build("youtube", "v3", developerKey=key, cache_discovery=False)
            self._thread_local.service_idx = self.current_key_index
        return self._thread_local.service
    
    def rotate_key(self):
        with self.index_lock:
            old_idx = self.current_key_index
            self.current_key_index = (self.current_key_index + 1) % len(self.keys)
            if self.current_key_index != old_idx:
                print(f"  [!] Rotating global API Key index to {self.current_key_index + 1}/{len(self.keys)}")
        
    def execute(self, request_creator):
        """Execute a request with automatic key rotation and thread-safe service management."""
        max_retries = len(self.keys) * 2 # Allow some retries for connection issues too
        retries = 0
        
        while retries < max_retries:
            try:
                service = self._get_service()
                request = request_creator(service)
                return request.execute()
            except HttpError as e:
                if e.resp.status in [403, 429]:
                    print(f"  [!] Quota limit hit for Key {self.current_key_index + 1}")
                    if len(self.keys) > 1:
                        self.rotate_key()
                        retries += 1
                        continue
                raise e
            except Exception as e:
                # Handle SSL, Timed out, IncompleteRead etc by forcing a service rebuild for this thread
                error_name = type(e).__name__
                if "timeout" in error_name.lower() or "ssl" in error_name.lower() or "read" in error_name.lower():
                    print(f"  [!] Connection error ({error_name}). Rebuilding thread service...")
                    if hasattr(self._thread_local, 'service_idx'):
                        del self._thread_local.service_idx
                    retries += 1
                    continue
                raise e
        raise Exception("Failed after multiple attempts due to quota or connection issues.")

# Global API instance
yt_api = YoutubeApi(YOUTUBE_API_KEYS)

# Global API instance
yt_api = YoutubeApi(YOUTUBE_API_KEYS)


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


def fetch_channel_videos(channel_id, channel_name, channel_tag="General"):

    """Fetch recent videos from a YouTube channel with optimization."""
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
            
        # Use yt_api.execute with lambda to support rotation
        channel_response = yt_api.execute(lambda s: s.channels().list(**kwargs))
        
        if not channel_response.get("items") and channel_id.startswith("UC"):
            print(f"  [X] ID failed for {channel_name}: {channel_id}")
            return []
                
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

    # Dynamic threshold: Specified hours relative to fetch time
    pub_after_date = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)

    # 1. Fetch video IDs from uploads playlist (stop when we hit old videos)
    video_ids = []
    next_page_token = None
    fetched_count = 0
    stop_fetching = False

    while fetched_count < MAX_RESULTS_PER_CHANNEL and not stop_fetching:
        try:
            # Use yt_api.execute with lambda to support rotation
            playlist_response = yt_api.execute(lambda s: s.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ))
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
            # Use yt_api.execute with lambda to support rotation
            video_response = yt_api.execute(lambda s: s.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(batch_ids)
            ))
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
                # Video is Live, skip per user request
                continue
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
                "channel_tag": channel_tag,
                "fetched_at": datetime.now(timezone.utc).isoformat()

            }
            videos.append(video_data)
    
    print(f"  [OK] {channel_name}: fetched {len(videos)} videos")
    return videos


def fetch_all_channels(targets=None):
    """Fetch videos from all configured channels in parallel."""
    print("=" * 60)
    print("  Optimized YouTube Data Fetcher (Parallel)")
    print("=" * 60)

    start_time = datetime.now()
    all_videos = []

    # Use ThreadPoolExecutor for parallel fetching
    if targets:
        target_channels = {}
        for t in targets:
            # Check if t is a name in CHANNEL_IDS
            if t in CHANNEL_IDS:
                target_channels[t] = CHANNEL_IDS[t]
            # Check if t is an actual ID (usually starts with UC)
            elif t.startswith("UC") or t.startswith("@"):
                target_channels[t] = t
            else:
                # Try case-insensitive name match
                found = False
                for name, cid in CHANNEL_IDS.items():
                    if name.lower() == t.lower():
                        target_channels[name] = cid
                        found = True
                        break
                if not found:
                    # If not found in config, assume it's a raw identifier
                    target_channels[t] = t
        
        print(f"  [INFO] Targeted Fetch: {', '.join(target_channels.keys())}")
    else:
        target_channels = CHANNEL_IDS

    with ThreadPoolExecutor(max_workers=CONCURRENT_THREADS) as executor:
        futures = {}
        for name, info in target_channels.items():
            cid = info["id"] if isinstance(info, dict) else info
            tag = info["tag"] if isinstance(info, dict) else "General"
            futures[executor.submit(fetch_channel_videos, cid, name, tag)] = name

        
        for future in futures:
            name = futures[future]
            try:
                results = future.result()
                all_videos.extend(results)
            except Exception as e:
                print(f"  [X] Exception for {name}: {e}")

    # Save to JSON (Atomic write using temp file)
    os.makedirs(DATA_DIR, exist_ok=True)
    temp_json = VIDEO_DATA_FILE + ".tmp"
    with open(temp_json, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "total_videos": len(all_videos),
            "channels": list(CHANNEL_IDS.keys()),
            "videos": all_videos
        }, f, ensure_ascii=False, indent=2)
    
    try:
        if os.path.exists(temp_json):
            shutil.move(temp_json, VIDEO_DATA_FILE)
    except Exception as e:
        print(f"  [X] Failed to save JSON atomically: {e}")
        # Final fallback
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
    import sys
    # Support: python fetch_data.py "Zee News" "ABP News"
    targets = sys.argv[1:] if len(sys.argv) > 1 else None
    fetch_all_channels(targets=targets)
