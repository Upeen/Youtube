# ============================================================
# YouTube Video Recommendation Engine
# Content-based filtering using TF-IDF + engagement scoring
# ============================================================

import json
import math
import re
from collections import Counter, defaultdict
from config import VIDEO_DATA_FILE, RECOMMENDATIONS_FILE


# Pre-compiled regex for performance
_CLEAN_RE = re.compile(r'[^\w\s]')
_SPACE_RE = re.compile(r'\s+')

# Common stop words
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'could', 'should', 'may', 'might', 'shall', 'can',
    'and', 'but', 'or', 'nor', 'not', 'so', 'yet', 'both',
    'either', 'neither', 'each', 'every', 'all', 'any', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'only',
    'same', 'than', 'too', 'very', 'just', 'because', 'as',
    'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how',
    'this', 'that', 'these', 'those', 'i', 'me', 'my', 'we',
    'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her',
    'it', 'its', 'they', 'them', 'their', 'what', 'which', 'who',
    'whom', 'if', 'into', 'ke', 'ki', 'ka', 'hai', 'ko', 'se',
    'ne', 'par', 'ye', 'mein', 'kya', 'hain', 'ya', 'ho',
    'video', 'subscribe', 'channel', 'like', 'share', 'comment',
}

class RecommendationEngine:
    """Content-based video recommendation engine."""

    def __init__(self):
        self.videos = []
        self.tfidf_matrix = {}
        self.idf_scores = {}
        self.vocab = set()
        self.fetched_at = ""

    def load_data(self):
        """Load video data from JSON file."""
        try:
            with open(VIDEO_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.videos = data.get("videos", [])
                self.fetched_at = data.get("fetched_at", "")
            print(f"[OK] Loaded {len(self.videos)} videos")
            return True
        except FileNotFoundError:
            print("[X] No video data found. Run fetch_data.py first.")
            return False
        except Exception as e:
            print(f"[X] Error loading data: {e}")
            return False

    def _tokenize(self, text):
        """Simple tokenizer: lowercase, remove special chars, split."""
        if not text:
            return []
        text = text.lower()
        text = _CLEAN_RE.sub(' ', text)
        text = _SPACE_RE.sub(' ', text).strip()
        tokens = text.split()
        return [t for t in tokens if len(t) > 1 and t not in STOP_WORDS]

    def _build_document(self, video):
        """Build a text document from video metadata."""
        parts = []
        # Title gets higher weight (repeated 3x)
        title = video.get("title", "")
        parts.extend([title] * 3)
        # Tags get medium weight (repeated 2x)
        tags = " ".join(video.get("tags", []))
        parts.extend([tags] * 2)
        # Description gets normal weight
        parts.append(video.get("description", ""))
        return " ".join(parts)

    def build_tfidf(self):
        """Build TF-IDF vectors for all videos."""
        # Build document frequency
        doc_freq = Counter()
        doc_tokens = {}

        for i, video in enumerate(self.videos):
            doc = self._build_document(video)
            tokens = self._tokenize(doc)
            doc_tokens[i] = tokens
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] += 1
                self.vocab.add(token)

        n_docs = len(self.videos)

        # Compute IDF
        self.idf_scores = {}
        for term, df in doc_freq.items():
            self.idf_scores[term] = math.log((n_docs + 1) / (df + 1)) + 1

        # Compute TF-IDF for each document
        self.tfidf_matrix = {}
        for i, tokens in doc_tokens.items():
            tf = Counter(tokens)
            total = len(tokens) if tokens else 1
            tfidf_vec = {}
            for term, count in tf.items():
                tf_val = count / total
                tfidf_vec[term] = tf_val * self.idf_scores.get(term, 0)
            # Normalize
            magnitude = math.sqrt(sum(v ** 2 for v in tfidf_vec.values())) or 1
            self.tfidf_matrix[i] = {k: v / magnitude for k, v in tfidf_vec.items()}

        print(f"[OK] Built TF-IDF matrix ({len(self.vocab)} unique terms)")

    def _cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between two sparse vectors."""
        common_terms = set(vec1.keys()) & set(vec2.keys())
        if not common_terms:
            return 0.0
        dot_product = sum(vec1[t] * vec2[t] for t in common_terms)
        return dot_product  # Already normalized

    def _engagement_score(self, video):
        """Calculate engagement score (0-1) based on views, likes, comments."""
        views = video.get("view_count", 0)
        likes = video.get("like_count", 0)
        comments = video.get("comment_count", 0)

        # Log-scale normalization
        view_score = math.log10(views + 1) / 8  # 100M views = 1.0
        like_score = math.log10(likes + 1) / 6   # 1M likes = 1.0
        comment_score = math.log10(comments + 1) / 5  # 100K comments = 1.0

        return min(1.0, (view_score * 0.4 + like_score * 0.35 + comment_score * 0.25))

    def _freshness_score(self, video):
        """Calculate freshness score (0-1), newer = higher."""
        age_hours = video.get("age_hours", 9999)
        if age_hours <= 6:
            return 1.0
        elif age_hours <= 24:
            return 0.9
        elif age_hours <= 72:
            return 0.7
        elif age_hours <= 168:  # 1 week
            return 0.5
        elif age_hours <= 720:  # 1 month
            return 0.3
        else:
            return 0.1

    def get_recommendations(self, video_id=None, top_n=12, channel="All", date_range=None, video_type="All", **kwargs):
        """Get video recommendations based on content similarity + engagement."""
        if not self.tfidf_matrix:
            self.build_tfidf()

        if video_id:
            # Find similar videos to a specific video
            target_idx = None
            for i, v in enumerate(self.videos):
                if v["video_id"] == video_id:
                    target_idx = i
                    break

            if target_idx is None:
                return []

            target_vec = self.tfidf_matrix.get(target_idx, {})
            scores = []
            for i, v in enumerate(self.videos):
                if i == target_idx:
                    continue
                if channel != "All" and v["channel_name"] != channel:
                    continue
                if video_type != "All" and v.get("video_type", "Video") != video_type:
                    continue
                if date_range and len(date_range) == 2:
                    pub_str = v.get("published_at", "")
                    if pub_str:
                        try:
                            from datetime import datetime as dt
                            pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
                            if not (date_range[0] <= pub_date <= date_range[1]):
                                continue
                        except Exception:
                            pass
                content_sim = self._cosine_similarity(target_vec, self.tfidf_matrix.get(i, {}))
                engagement = self._engagement_score(v)
                freshness = self._freshness_score(v)
                # Weighted final score
                final_score = (content_sim * 0.5) + (engagement * 0.3) + (freshness * 0.2)
                scores.append((i, final_score, content_sim, engagement, freshness))

            scores.sort(key=lambda x: x[1], reverse=True)
            results = []
            for idx, score, sim, eng, fresh in scores[:top_n]:
                v = self.videos[idx].copy()
                v["recommendation_score"] = round(score, 4)
                v["content_similarity"] = round(sim, 4)
                v["engagement_score"] = round(eng, 4)
                v["freshness_score"] = round(fresh, 4)
                results.append(v)
            return results
        else:
            # General trending recommendations
            scores = []
            for i, v in enumerate(self.videos):
                if channel != "All" and v["channel_name"] != channel:
                    continue
                if video_type != "All" and v.get("video_type", "Video") != video_type:
                    continue
                if date_range and len(date_range) == 2:
                    pub_str = v.get("published_at", "")
                    if pub_str:
                        try:
                            from datetime import datetime as dt
                            pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
                            if not (date_range[0] <= pub_date <= date_range[1]):
                                continue
                        except Exception:
                            pass
                engagement = self._engagement_score(v)
                freshness = self._freshness_score(v)
                final_score = (engagement * 0.6) + (freshness * 0.4)
                scores.append((i, final_score, engagement, freshness))

            scores.sort(key=lambda x: x[1], reverse=True)
            results = []
            for idx, score, eng, fresh in scores[:top_n]:
                v = self.videos[idx].copy()
                v["recommendation_score"] = round(score, 4)
                v["engagement_score"] = round(eng, 4)
                v["freshness_score"] = round(fresh, 4)
                results.append(v)
            return results

    def get_trending(self, top_n=10, channel="All", date_range=None, sort_by="trend_score", video_type="All", **kwargs):
        """Get trending videos using original Velocity + Engagement logic."""
        results = []
        for i, v in enumerate(self.videos):
            if channel != "All" and v["channel_name"] != channel:
                continue
            if video_type != "All" and v.get("video_type", "Video") != video_type:
                continue
            if date_range and len(date_range) == 2:
                pub_str = v.get("published_at", "")
                if pub_str:
                    try:
                        from datetime import datetime as dt
                        pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
                        if not (date_range[0] <= pub_date <= date_range[1]):
                            continue
                    except Exception:
                        pass
                
            views = v.get("view_count", 0)
            age = max(v.get("age_hours", 1), 1)
            velocity = views / age
            
            engagement = self._engagement_score(v)
            # Original Logic: 60% Velocity magnitude, 40% Engagement quality
            trend_score = (math.log10(velocity + 1) / 5) * 0.6 + engagement * 0.4
            
            v_copy = v.copy()
            v_copy["trend_score"] = round(trend_score, 4)
            v_copy["views_per_hour"] = round(velocity, 1)
            v_copy["engagement_score"] = round(engagement, 4)
            results.append(v_copy)

        sort_map = {
            "trend_score": "trend_score",
            "view_count": "view_count",
            "like_count": "like_count",
            "comment_count": "comment_count",
            "engagement_score": "engagement_score",
            "age_hours": "age_hours",
            "views_per_hour": "views_per_hour"
        }
        
        # Sort based on parameter
        s_key = sort_map.get(sort_by, "trend_score")
        if s_key == "age_hours":
            results.sort(key=lambda x: x.get(s_key, 9999))
        else:
            results.sort(key=lambda x: x.get(s_key, 0), reverse=True)

        return results[:top_n]

    def get_channel_stats(self):
        """Get aggregated stats per channel."""
        stats = defaultdict(lambda: {
            "total_videos": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "avg_engagement": 0,
            "channel_thumbnail": "",
            "channel_subscribers": 0
        })

        for v in self.videos:
            ch = v["channel_name"]
            stats[ch]["total_videos"] += 1
            stats[ch]["total_views"] += v.get("view_count", 0)
            stats[ch]["total_likes"] += v.get("like_count", 0)
            stats[ch]["total_comments"] += v.get("comment_count", 0)
            stats[ch]["channel_thumbnail"] = v.get("channel_thumbnail", "")
            stats[ch]["channel_subscribers"] = v.get("channel_subscribers", 0)

        for ch in stats:
            total = stats[ch]["total_videos"]
            if total > 0:
                total_engagement = stats[ch]["total_likes"] + stats[ch]["total_comments"]
                total_views = stats[ch]["total_views"]
                stats[ch]["avg_engagement"] = round(
                    (total_engagement / total_views * 100) if total_views > 0 else 0, 2
                )
                stats[ch]["avg_views"] = round(stats[ch]["total_views"] / total)

        return dict(stats)

    def search_videos(self, query, top_n=20, channel="All", date_range=None, video_type="All"):
        """Search videos by text query using TF-IDF similarity with filters."""
        if not self.tfidf_matrix:
            self.build_tfidf()

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        # Build query TF-IDF vector
        tf = Counter(query_tokens)
        total = len(query_tokens)
        query_vec = {}
        for term, count in tf.items():
            tf_val = count / total
            query_vec[term] = tf_val * self.idf_scores.get(term, 0)

        magnitude = math.sqrt(sum(v ** 2 for v in query_vec.values())) or 1
        query_vec = {k: v / magnitude for k, v in query_vec.items()}

        # Score all videos
        scores = []
        for i, v in enumerate(self.videos):
            if channel != "All" and v["channel_name"] != channel:
                continue
            if video_type != "All" and v.get("video_type", "Video") != video_type:
                continue
            if date_range and len(date_range) == 2:
                pub_str = v.get("published_at", "")
                if pub_str:
                    try:
                        from datetime import datetime as dt
                        pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
                        if not (date_range[0] <= pub_date <= date_range[1]):
                            continue
                    except Exception:
                        pass

            sim = self._cosine_similarity(query_vec, self.tfidf_matrix.get(i, {}))
            if sim > 0.01:
                scores.append((i, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:top_n]:
            v = self.videos[idx].copy()
            v["search_score"] = round(score, 4)
            results.append(v)
        return results


# Singleton instance
engine = RecommendationEngine()


def initialize():
    """Initialize the recommendation engine."""
    if engine.load_data():
        engine.build_tfidf()
        return True
    return False


if __name__ == "__main__":
    if initialize():
        print("\n--- Trending Videos ---")
        for v in engine.get_trending(5):
            print(f"  [{v['channel_name']}] {v['title'][:60]}... "
                  f"(score: {v['trend_score']}, views/hr: {v['views_per_hour']})")

        print("\n--- Top Recommendations ---")
        for v in engine.get_recommendations(top_n=5):
            print(f"  [{v['channel_name']}] {v['title'][:60]}... "
                  f"(score: {v['recommendation_score']})")
