import json
import os
from datetime import datetime, timezone

import streamlit as st

from recommender import RecommendationEngine
from config import VIDEO_DATA_FILE

PAGE_DASHBOARD = "Dashboard"
PAGE_TRENDING = "Trending"
PAGE_SEARCH = "Search"
PAGE_COVERAGE = "Coverage Race"
PAGE_DATA = "Raw Data"


st.set_page_config(
    page_title="YT Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --accent-red: #FF3D71;
        --accent-pink: #C850C0;
        --accent-purple: #4158D0;
        --accent-blue: #2BD2FF;
        --accent-green: #00E676;
        --accent-orange: #FF9A44;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050508 0%, #0a0a0f 100%);
        border-right: 1px solid rgba(255,255,255,0.03);
    }

    [data-testid="stSidebar"] .stMarkdown h1 {
        background: linear-gradient(135deg, #FF6B6B, #FF3D71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    /* Hide Sidebar Scrollbar */
    [data-testid="stSidebar"] section::-webkit-scrollbar {
        display: none;
    }
    [data-testid="stSidebar"] section {
        scrollbar-width: none;
        -ms-overflow-style: none;
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(10,10,15,0.95), rgba(15,15,22,0.95));
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), border-color 0.25s ease, box-shadow 0.25s ease;
        backdrop-filter: blur(10px);
        will-change: transform;
    }

    .stat-card:hover {
        border-color: rgba(255,255,255,0.15);
        transform: translate3d(0, -4px, 0);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.2;
    }

    .stat-label {
        font-size: 0.82rem;
        color: #9898b0;
        font-weight: 500;
        margin-top: 6px;
    }

    .gradient-text-red { background: linear-gradient(135deg, #FF6B6B, #FF3D71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-purple { background: linear-gradient(135deg, #4158D0, #C850C0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-green { background: linear-gradient(135deg, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-warm { background: linear-gradient(135deg, #FA8BFF, #2BD2FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .video-card {
        background: rgba(10, 10, 15, 0.98);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        overflow: hidden;
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease, box-shadow 0.25s ease;
        height: 100%;
        will-change: transform;
    }

    .video-card:hover {
        border-color: rgba(255,255,255,0.25);
        transform: translate3d(0, -6px, 0) scale(1.01);
        box-shadow: 0 15px 45px rgba(0,0,0,0.5), 0 0 40px rgba(200,80,192,0.15);
    }

    .video-thumb {
        width: 100%;
        aspect-ratio: 16/9;
        object-fit: cover;
        border-radius: 14px 14px 0 0;
    }

    .video-body {
        padding: 16px;
    }

    .video-title {
        font-size: 0.88rem;
        font-weight: 600;
        line-height: 1.4;
        margin-bottom: 8px;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        color: #f0f0f5;
    }

    .video-channel {
        font-size: 0.78rem;
        color: #9898b0;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .video-stats {
        display: flex;
        gap: 12px;
        font-size: 0.75rem;
        color: #f0f0f5;
        flex-wrap: wrap;
        font-weight: 600;
    }

    .video-stats span {
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 8px;
    }

    .badge-trend {
        background: linear-gradient(135deg, #FF9A44, #FF3D71);
        color: white;
    }

    .badge-score {
        background: linear-gradient(135deg, #4158D0, #C850C0);
        color: white;
    }

    .badge-match {
        background: linear-gradient(135deg, #00C9FF, #92FE9D);
        color: #0a0a0f;
    }

    .badge-type-live {
        background: linear-gradient(135deg, #FF0000, #FF4500);
        color: white;
    }

    .badge-type-short {
        background: linear-gradient(135deg, #8E2DE2, #4A00E0);
        color: white;
    }

    .badge-type-video {
        background: rgba(255,255,255,0.1);
        color: #9898b0;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .channel-card {
        background: rgba(22, 22, 31, 0.85);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 28px;
        transition: transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1), border-color 0.25s ease, box-shadow 0.25s ease;
        position: relative;
        overflow: hidden;
        will-change: transform;
    }

    .channel-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(135deg, #4158D0, #C850C0);
    }

    .channel-card:hover {
        border-color: rgba(255,255,255,0.2);
        transform: translate3d(0, -4px, 0);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 20px rgba(65,88,208,0.15);
    }

    .channel-name {
        font-size: 1.15rem;
        font-weight: 700;
        margin-bottom: 4px;
        color: #f0f0f5;
    }

    .channel-subs {
        font-size: 0.78rem;
        color: #5e5e78;
        margin-bottom: 16px;
    }

    .ch-stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }

    .ch-stat-box {
        background: rgba(26, 26, 38, 0.8);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    
    .ch-stat-box:hover {
        background: rgba(35, 35, 50, 0.9);
        transform: translateY(-2px);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .ch-stat-val {
        font-size: 1.1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FA8BFF, #2BD2FF, #2BFF88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .ch-stat-label {
        font-size: 0.7rem;
        color: #f0f0f5;
        margin-top: 4px;
        font-weight: 600;
        opacity: 0.8;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        color: #f0f0f5;
    }

    .section-subtitle {
        font-size: 0.88rem;
        color: #9898b0;
        margin-bottom: 24px;
    }

    .tag-pill {
        display: inline-block;
        font-size: 0.68rem;
        padding: 3px 10px;
        background: rgba(65, 88, 208, 0.15);
        color: #2BD2FF;
        border-radius: 20px;
        margin: 2px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .tag-pill:hover {
        background: rgba(65, 88, 208, 0.35);
        transform: translateY(-1px);
        color: #ffffff;
    }

    @keyframes float1 {
        0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
        50% { transform: translate3d(0, -30px, 0) scale(1.05); }
    }
    
    @keyframes float2 {
        0%, 100% { transform: translate3d(0, 0, 0) scale(1); }
        50% { transform: translate3d(0, 30px, 0) scale(0.95); }
    }

    @keyframes fadeInSlideUp {
        from { opacity: 0; transform: translate3d(0, 15px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    .video-card, .stat-card, .channel-card {
        animation: fadeInSlideUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: -10%;
        right: -5%;
        width: 500px;
        height: 500px;
        background: #FF3D71;
        border-radius: 50%;
        filter: blur(150px);
        opacity: 0.06;
        pointer-events: none;
        z-index: 0;
        animation: float1 15s ease-in-out infinite;
    }

    .stApp::after {
        content: '';
        position: fixed;
        bottom: -10%;
        left: -5%;
        width: 400px;
        height: 400px;
        background: #4158D0;
        border-radius: 50%;
        filter: blur(140px);
        opacity: 0.06;
        pointer-events: none;
        z-index: 0;
        animation: float2 18s ease-in-out infinite;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    a.video-link {
        color: #FF3D71;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.82rem;
        transition: color 0.2s;
    }

    a.video-link:hover {
        color: #FF6B6B;
    }

    hr {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 24px 0;
    }

    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 0.9rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def format_number(num):
    if num is None:
        return "0"
    if num >= 10_000_000:
        return f"{num / 10_000_000:.1f} Cr"
    if num >= 100_000:
        return f"{num / 100_000:.1f} L"
    if num >= 1000:
        return f"{num / 1000:.1f}K"
    return f"{num:,}"


def time_ago(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        diff = datetime.now(timezone.utc) - dt
        secs = int(diff.total_seconds())
        if secs < 60:
            return "just now"
        if secs < 3600:
            return f"{secs // 60}m ago"
        if secs < 86400:
            return f"{secs // 3600}h ago"
        if secs < 604800:
            return f"{secs // 86400}d ago"
        if secs < 2592000:
            return f"{secs // 604800}w ago"
        return f"{secs // 2592000}mo ago"
    except Exception:
        return ""


def render_stat_card(value, label, gradient_class):
    return f"""
    <div class="stat-card">
        <div class="stat-value {gradient_class}">{value}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def render_video_card(video, badge_type=None, badge_text=None, show_eng_rate=False):
    badge_html = f'<div class="badge badge-{badge_type}">{badge_text}</div>' if badge_type and badge_text else ""

    # Video Type Badge
    vtype = video.get("video_type", "Video")
    vtype_class = f"badge-type-{vtype.lower()}"
    type_badge_html = f'<div class="badge {vtype_class}" style="margin-left:5px">{vtype}</div>'

    tags_html = "".join(f'<span class="tag-pill">{tag}</span>' for tag in video["tags"][:5]) if video.get("tags") else ""
    tags_div = f'\n            <div style="margin-top:8px">{tags_html}</div>' if tags_html else ""

    # Parse Exact Timestamp
    published_raw = video.get('published_at', '')
    published_date = published_raw[:10] if published_raw else 'Unknown Date'
    
    date_display = f"Published {published_date} ({time_ago(published_raw)})"
    eng_rate_span = f"\n                <span><b>Eng. Rate</b> {video.get('engagement_rate', 0):.2f}%</span>" if show_eng_rate else ""

    return f"""<div class="video-card">
<img class="video-thumb" src="{video.get('thumbnail', '')}" alt="" loading="lazy" onerror="this.style.background='#16161f';this.style.minHeight='160px'">
<div class="video-body">
<div style="display:flex; align-items:center; margin-bottom: 8px;">
{badge_html}{type_badge_html}
</div>
<div class="video-title">{video.get('title', '')}</div>
<div class="video-channel">{video.get('channel_name', '')} &middot; {video.get('duration_formatted', '')}</div>
<div class="video-stats">
<span><b>Views</b> {format_number(video.get('view_count', 0))}</span>
<span><b>Likes</b> {format_number(video.get('like_count', 0))}</span>
<span><b>Comments</b> {format_number(video.get('comment_count', 0))}</span>{eng_rate_span}
<span>{date_display}</span>
</div>{tags_div}
<div style="margin-top:10px">
<a class="video-link" href="{video.get('url', '#')}" target="_blank">Watch on YouTube</a>
</div>
</div>
</div>"""


def render_channel_card(name, stats):
    return f"""
    <div class="channel-card">
        <div class="channel-name">{name}</div>
        <div class="channel-subs">{format_number(stats.get('channel_subscribers', 0))} subscribers</div>
        <div class="ch-stat-grid">
            <div class="ch-stat-box">
                <div class="ch-stat-val">{stats.get('total_videos', 0)}</div>
                <div class="ch-stat-label"><b>Videos</b></div>
            </div>
            <div class="ch-stat-box">
                <div class="ch-stat-val">{format_number(stats.get('total_views', 0))}</div>
                <div class="ch-stat-label"><b>Total Views</b></div>
            </div>
            <div class="ch-stat-box">
                <div class="ch-stat-val">{format_number(stats.get('total_likes', 0))}</div>
                <div class="ch-stat-label"><b>Total Likes</b></div>
            </div>
            <div class="ch-stat-box">
                <div class="ch-stat-val">{stats.get('avg_engagement', 0)}%</div>
                <div class="ch-stat-label"><b>Engagement</b></div>
            </div>
        </div>
    </div>
    """


@st.cache_resource
def load_engine():
    engine = RecommendationEngine()
    if engine.load_data() and engine.videos:
        engine.build_tfidf()
        return engine
    return None


engine = load_engine()


def get_local_filters(key_prefix):
    import datetime
    from datetime import timedelta
    
    with st.expander("🔍 Filters & Tools", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            today = datetime.date.today()
            date_range = st.date_input(
                "Date Range",
                value=(today, today),
                help="Filter videos by publication date",
                key=f"{key_prefix}_date"
            )
            
        with col2:
            all_channels = ["All"]
            if os.path.exists(VIDEO_DATA_FILE):
                try:
                    with open(VIDEO_DATA_FILE, "r", encoding="utf-8") as f:
                        d = json.load(f)
                        all_channels += sorted(list(set(v["channel_name"] for v in d.get("videos", []))))
                except:
                    pass
            channel = st.selectbox("Channel", all_channels, key=f"{key_prefix}_channel")
            
        with col3:
            vt = st.selectbox("Video Type", ["All", "Video", "Short", "Live"], key=f"{key_prefix}_vt")
            
    return date_range, channel, vt


with st.sidebar:
    st.markdown("# 🎯 YT Recommender")
    st.caption("AI-Powered YouTube Recommendations")
    
    # Show Last Refreshed & Data Coverage
    if engine and engine.fetched_at:
        try:
            # The timestamp is saved in UTC
            dt_utc = datetime.fromisoformat(engine.fetched_at.replace("Z", "+00:00"))
            # Convert to local timezone
            dt_local = dt_utc.astimezone(None)
            refresh_time = dt_local.strftime("%Y-%m-%d %I:%M %p")
            st.info(f"💾 **Last Refresh (Local):**\n{refresh_time}")
        except:
            st.info(f"💾 **Last Refresh:**\n{engine.fetched_at[:19]}")
    elif not engine:
        st.warning("⚠️ No data loaded yet.")

    st.divider()

    page = st.radio(
        "Navigate",
        [PAGE_DASHBOARD, PAGE_TRENDING, PAGE_SEARCH, PAGE_COVERAGE, PAGE_DATA],
        label_visibility="collapsed",
    )

    st.divider()

    if st.button("🚀 Fetch Fresh Data", use_container_width=True, type="primary"):
        with st.status("Fetching latest data...", expanded=True) as status:
            st.write("Initializing Optimized Parallel Fetcher...")
            try:
                from fetch_data import fetch_all_channels
                videos = fetch_all_channels()
                st.write(f"Successfully fetched {len(videos)} videos!")
                st.cache_resource.clear()
                status.update(label="Fetch Complete!", state="complete", expanded=False)
                st.rerun()
            except Exception as exc:
                st.error(f"Could not fetch data: {exc}")
                status.update(label="Fetch Failed", state="error")
    
    st.caption("v2.0 Optimized Parallel Fetcher")




if engine is None:
    st.markdown(
        """
    <div style="text-align:center; padding:80px 20px;">
        <h1 style="font-size:3rem; margin-bottom:16px;">🎯</h1>
        <h2>Welcome to YT Recommender</h2>
        <p style="color:#9898b0; margin-top:8px;">
            Click <strong>Fetch Fresh Data</strong> in the sidebar to get started.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    # Even if engine is None, we still want the sidebar for "Fetch Fresh Data"
    # So we don't st.stop() immediately if we are in the middle of a fetch or first run


if page == PAGE_DASHBOARD:
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Overview of your YouTube analytics</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt = get_local_filters("dash")

    st.markdown("---")

    # ── FULL WIDTH TRENDING ──────────────────────────────────────────
    st.markdown("### 🔥 Top Viral Trends (Top 50)")
    trending = engine.get_trending(50, channel=local_channel, date_range=local_date_range, video_type=local_vt)
    
    if trending:
        tcols = st.columns(3)
        for index, video in enumerate(trending, start=1):
            with tcols[(index-1) % 3]:
                badge_text = f"#{index} Viral | {format_number(video.get('views_per_hour', 0))} VPH"
                st.markdown(render_video_card(video, "trend", badge_text, show_eng_rate=True), unsafe_allow_html=True)
                st.markdown("")
    else:
        st.info("No trending data available for the current filters.")

elif page == PAGE_TRENDING:
    st.markdown('<div class="section-title">Trending Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Videos gaining the most traction right now</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt = get_local_filters("trend")

    col1, col2 = st.columns(2)
    with col1:
        limit = st.slider("Number of videos", 5, 50, 20, key="trend_limit")
    with col2:
        sort_opts = {
            "Trending Score": "trend_score", 
            "Views/Hr": "views_per_hour",
            "Total Views": "view_count", 
            "Likes": "like_count", 
            "Comments": "comment_count", 
            "Engagement Rate": "engagement_score", 
            "Newest": "age_hours"
        }
        selected_sort_label = st.selectbox("Sort By", list(sort_opts.keys()), key="trend_sort")
        sort_key = sort_opts[selected_sort_label]

    trending = engine.get_trending(
        limit, 
        channel=local_channel, 
        date_range=local_date_range, 
        sort_by=sort_key, 
        video_type=local_vt
    )

    cols = st.columns(3)
    for index, video in enumerate(trending, start=1):
        with cols[(index - 1) % 3]:
            badge_text = f"#{index} Trending | {format_number(video.get('views_per_hour', 0))} views/hr"
            st.markdown(render_video_card(video, "trend", badge_text, show_eng_rate=True), unsafe_allow_html=True)
            st.markdown("")


    video_options = {f"{video['title'][:70]}... ({video['channel_name']})": video["video_id"] for video in engine.videos}
    selected = st.selectbox("Choose a video", list(video_options.keys()), key="similar_select")

    if selected:
        video_id = video_options[selected]
        similar = engine.get_recommendations(video_id=video_id, top_n=6)

        if similar:
            sim_cols = st.columns(3)
            for index, video in enumerate(similar):
                with sim_cols[index % 3]:
                    score = video.get("content_similarity", 0)
                    st.markdown(
                        render_video_card(video, "match", f"Match: {score:.0%}"),
                        unsafe_allow_html=True,
                    )
                    st.markdown("")
        else:
            st.info("No similar videos found.")


elif page == PAGE_SEARCH:
    st.markdown('<div class="section-title">Search Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Find videos across all channels using AI-powered search</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt = get_local_filters("search")

    query = st.text_input("Search query", placeholder="Type keywords...", key="search_q")

    if query:
        results = engine.search_videos(query, top_n=24, channel=local_channel, date_range=local_date_range, video_type=local_vt)

        if results:
            st.success(f'Found {len(results)} results for "{query}"')
            cols = st.columns(3)
            for index, video in enumerate(results):
                with cols[index % 3]:
                    match = video.get("search_score", 0)
                    st.markdown(
                        render_video_card(video, "match", f"Match: {match:.0%}"),
                        unsafe_allow_html=True,
                    )
                    st.markdown("")
        else:
            st.warning(f'No results found for "{query}"')
    else:
        st.markdown(
            """
        <div style="text-align:center; padding:60px 20px; color:#5e5e78;">
            <div style="font-size:3rem; margin-bottom:12px;">🔍</div>
            <p>Enter a query to search across all video titles, descriptions, and tags</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


elif page == PAGE_DATA:
    st.markdown('<div class="section-title">📊 Raw Data Explorer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Comprehensive list of all videos with full metrics and URLs</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt = get_local_filters("raw_data")

    # ── Filtering Logic ───────────────────────────────────────────────
    filtered = engine.videos.copy()
    
    if local_channel != "All":
        filtered = [v for v in filtered if v["channel_name"] == local_channel]
    
    if local_vt != "All":
        filtered = [v for v in filtered if v.get("video_type", "Video") == local_vt]
        
    if local_date_range and len(local_date_range) == 2:
        from datetime import datetime as dt
        start_date, end_date = local_date_range
        filtered_by_date = []
        for v in filtered:
            pub_str = v.get("published_at", "")
            if pub_str:
                try:
                    pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
                    if start_date <= pub_date <= end_date:
                        filtered_by_date.append(v)
                except:
                    pass
        filtered = filtered_by_date

    st.markdown(f"### 📑 Dataset ({len(filtered)} videos)")
    
    if not filtered:
        st.info("No videos found matching the current filters.")
    else:
        # Prepare data for display
        display_data = []
        import math
        for v in filtered:
            # Pre-calculate velocity for display
            age_hours = max(v.get("age_hours", 1), 1)
            velocity = v.get("view_count", 0) / age_hours
            
            # Calculate scores using engine methods if they exist
            eng_score = engine._engagement_score(v)
            fresh_score = engine._freshness_score(v)
            trend_score = (math.log10(velocity + 1) / 5) * 0.6 + eng_score * 0.4
            
            display_data.append({
                "Published": v.get("published_at", "")[:10],
                "Channel": v.get("channel_name", ""),
                "Title": v.get("title", ""),
                "Type": v.get("video_type", "Video"),
                "Views": v.get("view_count", 0),
                "Velocity (VPH)": round(velocity, 2),
                "Likes": v.get("like_count", 0),
                "Comments": v.get("comment_count", 0),
                "Eng. Rate (%)": round(v.get("engagement_rate", 0), 2),
                "Eng. Score": round(eng_score, 4),
                "Freshness": round(fresh_score, 4),
                "Trend Score": round(trend_score, 4),
                "Duration": v.get("duration_formatted", ""),
                "Tags": ", ".join(v.get("tags", [])) if v.get("tags") else "",
                "URL": v.get("url", ""),
                "Video ID": v.get("video_id", "")
            })

        import pandas as pd
        df = pd.DataFrame(display_data)
        
        # Sort by most recent by default
        df = df.sort_values("Published", ascending=False)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "URL": st.column_config.LinkColumn("Watch Link", display_text="Open"),
                "Views": st.column_config.NumberColumn(format="%d"),
                "Velocity (VPH)": st.column_config.NumberColumn(format="%.1f"),
                "Eng. Rate (%)": st.column_config.ProgressColumn(
                    "Eng. Rate (%)",
                    format="%.2f%%",
                    min_value=0,
                    max_value=20,
                ),
                "Trend Score": st.column_config.NumberColumn(format="%.4f"),
                "Eng. Score": st.column_config.NumberColumn(format="%.4f"),
                "Freshness": st.column_config.NumberColumn(format="%.4f"),
            }
        )

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Raw Data (CSV)",
            data=csv,
            file_name=f"youtube_raw_data_{local_channel}.csv",
            mime='text/csv',
        )

elif page == PAGE_COVERAGE:
    import re
    from collections import defaultdict
    from datetime import datetime as dt

    st.markdown('<div class="section-title">🏁 Coverage Race</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Identify which channels broke a story first — and by how many minutes</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt = get_local_filters("coverage")

    # ── Topic search ──────────────────────────────────────────────────
    topic_query = st.text_input(
        "🔎 Enter a topic or keyword (e.g. 'Modi', 'Budget', 'Pakistan')",
        placeholder="Type a breaking news keyword...",
        key="coverage_query",
    )

    # Use local filters instead of separate inputs if possible, or keep them for finer control
    # The user wanted local filters in each tab.
    cov_start, cov_end = local_date_range if (local_date_range and len(local_date_range) == 2) else (None, None)


    if not topic_query:
        st.markdown(
            """<div style="text-align:center;padding:60px 20px;color:#5e5e78;">
            <div style="font-size:3rem;margin-bottom:12px;">🏁</div>
            <p>Enter a topic keyword above to see which channels covered it first</p>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        # ── Fetch relevant videos ─────────────────────────────────────
        query_tokens = set(re.sub(r"[^\w\s]", " ", topic_query.lower()).split())

        matched = []
        for v in engine.videos:
            # Date filter
            pub_str = v.get("published_at", "")
            if not pub_str:
                continue
            try:
                pub_date = dt.fromisoformat(pub_str.replace("Z", "+00:00")).date()
            except Exception:
                continue
            if not (cov_start <= pub_date <= cov_end):
                continue

            # Channel filter
            if local_channel != "All" and v.get("channel_name") != local_channel:
                continue
            
            # Video type filter
            if local_vt != "All" and v.get("video_type", "Video") != local_vt:
                continue

            # Keyword match in title + tags (All tokens must match for combination search)
            title_text = v.get("title", "").lower()
            tags_text  = " ".join(v.get("tags", [])).lower()
            combined   = title_text + " " + tags_text
            
            # Check if ALL keywords are present (The "Combination" logic)
            if all(tok in combined for tok in query_tokens if len(tok) > 2):
                matched.append(v)

        if not matched:
            st.warning(f'No videos found for **"{topic_query}"** in the selected date range.')
        else:
            # ── Sort by publish time ──────────────────────────────────
            matched.sort(key=lambda v: v.get("published_at", ""))

            # ── Parse timestamps ──────────────────────────────────────
            def parse_ts(pub_str):
                try:
                    return dt.fromisoformat(pub_str.replace("Z", "+00:00"))
                except Exception:
                    return None

            first_ts   = parse_ts(matched[0].get("published_at", ""))
            first_chan  = matched[0].get("channel_name", "Unknown")

            st.success(f'Found **{len(matched)}** videos covering **"{topic_query}"** — '
                       f'First reported by **{first_chan}** at `{first_ts.strftime("%Y-%m-%d %H:%M") if first_ts else "N/A"}` IST')

            st.markdown("---")

            # ── WINNER PODIUM (top-3 fastest) ─────────────────────────
            st.markdown("### 🥇 Channel Speed Podium")
            # One video per channel — the earliest one; also count stories per channel
            channel_first: dict = {}
            channel_story_count: dict = {}
            for v in matched:
                ch = v.get("channel_name", "Unknown")
                channel_story_count[ch] = channel_story_count.get(ch, 0) + 1
                if ch not in channel_first:
                    channel_first[ch] = v

            podium_list = sorted(
                channel_first.items(),
                key=lambda x: x[1].get("published_at", "")
            )

            medal_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
            medal_icons  = ["🥇", "🥈", "🥉"]

            # Display all channels in a grid (4 columns wide)
            cols_per_row = 4
            num_channels = len(podium_list)
            
            for i in range(0, num_channels, cols_per_row):
                row_channels = podium_list[i : i + cols_per_row]
                row_cols = st.columns(cols_per_row)
                
                for idx, (ch, v) in enumerate(row_channels):
                    total_idx = i + idx
                    ts = parse_ts(v.get("published_at", ""))
                    delay_mins = round((ts - first_ts).total_seconds() / 60) if ts and first_ts else 0
                    
                    # Medal logic for top 3
                    medal_color = medal_colors[total_idx] if total_idx < 3 else "#2d2d3d"
                    medal_icon = medal_icons[total_idx] if total_idx < 3 else "📺"
                    
                    with row_cols[idx]:
                        story_count = channel_story_count.get(ch, 0)
                        st.markdown(
                            f"""<div class="stat-card" style="border-color:{medal_color};border-width:2px; height:100%;">
                            <div class="stat-value" style="font-size:2.2rem;">{medal_icon}</div>
                            <div class="stat-value gradient-text-warm" style="font-size:1rem;margin-top:6px;">{ch}</div>
                            <div class="stat-label" style="margin-top:6px;">{ts.strftime('%H:%M, %d %b') if ts else 'N/A'}</div>
                            <div class="stat-label">{"🚀 First!" if delay_mins == 0 else f"+{delay_mins} min late"}</div>
                            <div class="stat-label">📰 {story_count} {'story' if story_count == 1 else 'stories'}</div>
                            </div>""",
                            unsafe_allow_html=True,
                        )

            st.markdown("---")

            # ── TIMELINE TABLE ────────────────────────────────────────
            st.markdown("### ⏱ Full Coverage Timeline")

            timeline_rows = []
            for rank, (ch, v) in enumerate(podium_list, start=1):
                ts = parse_ts(v.get("published_at", ""))
                delay_mins = round((ts - first_ts).total_seconds() / 60) if ts and first_ts else 0
                delay_hrs  = delay_mins // 60
                delay_rem  = delay_mins % 60

                if delay_mins == 0:
                    delay_str = "🚀 First!"
                elif delay_hrs > 0:
                    delay_str = f"+{delay_hrs}h {delay_rem}m"
                else:
                    delay_str = f"+{delay_mins}m"

                timeline_rows.append({
                    "Rank": rank,
                    "Channel": ch,
                    "Published At (First)": ts.strftime("%Y-%m-%d %H:%M") if ts else "N/A",
                    "Time Gap": delay_str,
                    "Stories": channel_story_count.get(ch, 0),
                    "Views (First Video)": format_number(v.get("view_count", 0)),
                    "Likes": format_number(v.get("like_count", 0)),
                    "Eng. Rate": f"{v.get('engagement_rate', 0):.2f}%",
                    "Video Type": v.get("video_type", "Video"),
                    "Title (First Video)": v.get("title", "")[:70],
                })

            st.dataframe(timeline_rows, use_container_width=True, hide_index=True)

            st.markdown("---")

            # ── ALL MATCHING VIDEOS (chronological feed table) ─────────
            st.markdown(f"### 📺 All {len(matched)} Videos — Chronological Feed")

            feed_data = []
            for v in matched:
                ts = parse_ts(v.get("published_at", ""))
                ref_ts = first_ts
                delay_mins = round((ts - ref_ts).total_seconds() / 60) if ts and ref_ts else 0

                if delay_mins == 0:
                    delay_label = "🚀 FIRST"
                else:
                    hrs = delay_mins // 60
                    mins = delay_mins % 60
                    delay_label = f"+{hrs}h {mins}m" if hrs > 0 else f"+{mins}m"

                feed_data.append({
                    "Time Gap": delay_label,
                    "Channel": v.get("channel_name", ""),
                    "Published At": ts.strftime("%H:%M, %d %b") if ts else "",
                    "Title": v.get("title", ""),
                    "Views": v.get("view_count", 0),
                    "Video Link": v.get("url", ""),
                })

            st.dataframe(
                feed_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Video Link": st.column_config.LinkColumn("Watch", display_text="Open YouTube"),
                    "Views": st.column_config.NumberColumn(format="%d"),
                    "Time Gap": st.column_config.TextColumn("Gap", width="small")
                }
            )
