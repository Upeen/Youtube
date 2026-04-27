import json
import os
from datetime import datetime, timezone

import streamlit as st
import pandas as pd

from recommender import RecommendationEngine
from config import VIDEO_DATA_FILE

PAGE_DASHBOARD = "Dashboard"
PAGE_TRENDING = "Trending"
PAGE_SEARCH = "Search"
PAGE_COVERAGE = "Coverage Race"
PAGE_DATA = "Raw Data"
PAGE_RECENT = "Recent News"



st.set_page_config(
    page_title="YT Recommender",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- AUTHENTICATION LOGIC ---
def check_authentication():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Load the master key for comparison
        master_key_path = os.path.join(os.path.dirname(__file__), "private_key.json")
        master_key = None
        if os.path.exists(master_key_path):
            with open(master_key_path, "r") as f:
                master_key = json.load(f)
        
        st.markdown("""
            <div style="text-align:center; padding: 100px 20px;">
                <h1 style="background: linear-gradient(135deg, #FF6B6B, #FF3D71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin-bottom: 20px;">
                    🔐 Secured Access
                </h1>
                <p style="color: #9898b0; font-size: 1.1rem; max-width: 600px; margin: 0 auto 40px auto;">
                    This dashboard is restricted. Please upload your <b>Private Key (JSON)</b> file to verify your identity and unlock the analytics suite.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader("Upload Private Key JSON", type=['json'])
            
            if uploaded_file is not None:
                try:
                    payload = json.load(uploaded_file)
                    # Unified Validation
                    if master_key:
                        is_valid = (
                            payload.get("private_key") == master_key.get("private_key") and
                            payload.get("project_id") == master_key.get("project_id")
                        )
                    else:
                        is_valid = payload.get("private_key") == "Devidpl@11491750"
                    
                    if is_valid:
                        st.session_state.authenticated = True
                        st.success("Authentication Successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid Private Key. Access Denied.")
                except Exception as e:
                    st.error(f"Error parsing JSON: {str(e)}")
        
        st.stop() # Stop execution if not authenticated

check_authentication()

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --accent-red: #FF3D71;
        --accent-pink: #C850C0;
        --accent-purple: #4158D0;
        --accent-blue: #2BD2FF;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050508 0%, #0a0a0f 100%);
        border-right: 1px solid rgba(255,255,255,0.03);
    }

    [data-testid="stSidebar"] section::-webkit-scrollbar {
        display: none;
    }

    [data-testid="stSidebar"] .stMarkdown h1 {
        background: linear-gradient(135deg, #FF6B6B, #FF3D71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 61, 113, 0.4); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 61, 113, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 61, 113, 0); }
    }

    .stat-card {
        background: linear-gradient(135deg, rgba(10,10,15,0.95), rgba(15,15,22,0.95));
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.6s ease-out forwards;
    }

    .stat-card:hover {
        border-color: rgba(255,61,113,0.3);
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .stat-value {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .stat-label {
        font-size: 0.72rem;
        color: #9898b0;
    }

    .video-card {
        background: rgba(10, 10, 15, 0.98);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 14px;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        height: 100%;
        animation: fadeInUp 0.8s ease-out forwards;
    }

    .video-card:hover {
        border-color: rgba(255,255,255,0.2);
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }

    .badge-trend {
        background: linear-gradient(135deg, #FF3D71 0%, #FF6B6B 100%);
        color: white !important;
        box-shadow: 0 4px 12px rgba(255, 61, 113, 0.3);
        animation: pulse 2s infinite;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .video-thumb {
        width: 100%;
        aspect-ratio: 16/9;
        object-fit: cover;
        transition: transform 0.6s ease;
    }

    .video-card:hover .video-thumb {
        transform: scale(1.1);
    }

    .video-body { padding: 16px; }

    .video-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #f0f0f5;
        margin-bottom: 6px;
    }

    .video-channel {
        font-size: 0.72rem;
        color: #9898b0;
        font-weight: 500;
        margin-bottom: 6px;
    }

    .video-stats {
        display: flex;
        gap: 10px;
        font-size: 0.68rem;
        color: #f0f0f5;
        flex-wrap: wrap;
        font-weight: 600;
    }

    .badge {
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }

    .gradient-text-red { background: linear-gradient(135deg, #FF6B6B, #FF3D71); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-purple { background: linear-gradient(135deg, #4158D0, #C850C0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-green { background: linear-gradient(135deg, #00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .gradient-text-warm { background: linear-gradient(135deg, #FA8BFF, #2BD2FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    .tag-pill {
        display: inline-block;
        font-size: 0.68rem;
        padding: 2px 8px;
        background: rgba(255, 61, 113, 0.1);
        color: #FF3D71;
        border-radius: 4px;
        margin: 2px;
        font-weight: 600;
    }

    a.video-link {
        color: #FF3D71;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.82rem;
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: -10%;
        right: -5%;
        width: 500px;
        height: 500px;
        background: #FF3D71;
        filter: blur(150px);
        opacity: 0.05;
        pointer-events: none;
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


def time_ago(dt_val):
    if dt_val is None or dt_val == "":
        return ""
    try:
        # Handle string input
        if isinstance(dt_val, str):
            dt = datetime.fromisoformat(dt_val.replace("Z", "+00:00"))
        else:
            # Handle datetime/Timestamp objects
            dt = dt_val
            
        # Ensure timezone awareness for comparison
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
            
        diff = datetime.now(timezone.utc) - dt
        secs = int(diff.total_seconds())
        if secs < 0: secs = 0 # Future-proof
        
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

    # Channel Category Badge
    vcat = video.get("channel_tag", "General")
    cat_badge_html = f'<div class="badge" style="margin-left:5px; background: rgba(255,255,255,0.1); color: #f0f0f5;">{vcat}</div>'


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
{badge_html}{type_badge_html}{cat_badge_html}
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


@st.cache_resource(ttl=50, show_spinner=False)
def load_engine():
    engine = RecommendationEngine()
    if engine.load_data() and engine.videos:
        engine.build_tfidf()
        return engine
    return None


@st.cache_data(ttl=50, show_spinner=False)
def get_cached_trending(_engine, limit, channel, date_range, sort_by, video_type, category):
    return _engine.get_trending(limit, channel=channel, date_range=date_range, sort_by=sort_by, video_type=video_type, category=category)



@st.cache_data(ttl=50, show_spinner=False)
def get_cached_search(_engine, query, top_n, channel, date_range, video_type, category):
    return _engine.search_videos(query, top_n=top_n, channel=channel, date_range=date_range, video_type=video_type, category=category)



@st.cache_data(ttl=50, show_spinner=False)
def cached_fetch_data():
    from fetch_data import fetch_all_channels
    return fetch_all_channels()


engine = load_engine()


def get_local_filters(key_prefix):
    import datetime
    from datetime import timedelta
    
    with st.expander("🔍 Filters & Tools", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            today = datetime.date.today()
            date_range = st.date_input(
                "Date Range",
                value=(today, today),
                help="Filter videos by publication date",
                key=f"{key_prefix}_date"
            )

        # Pre-load data to get tags and filter channels
        all_vids = []
        if os.path.exists(VIDEO_DATA_FILE):
            try:
                with open(VIDEO_DATA_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                    all_vids = d.get("videos", [])
            except:
                pass

        all_tags = sorted(list(set(v.get("channel_tag", "General") for v in all_vids)))
        all_tags = ["All"] + all_tags

        with col2:
            cat = st.selectbox("Category", all_tags, key=f"{key_prefix}_cat")
            
        with col3:
            # Filter channels based on selected category
            if cat == "All":
                filtered_vids = all_vids
            else:
                filtered_vids = [v for v in all_vids if v.get("channel_tag", "General") == cat]
            
            chan_list = sorted(list(set(v["channel_name"] for v in filtered_vids)))
            all_channels = ["All"] + chan_list
            channel = st.selectbox("Channel", all_channels, key=f"{key_prefix}_channel")
            
        with col4:
            vt = st.selectbox("Video Type", ["All", "Video", "Short"], key=f"{key_prefix}_vt")
            
    return date_range, channel, vt, cat




def get_recent_filters(key_prefix):
    import datetime
    from datetime import timedelta
    
    with st.expander("🔍 Filters & Tools", expanded=True):
        cols = st.columns(3)
        
        with cols[0]:
            vt = st.selectbox("Video Type", ["All", "Video", "Short"], key=f"{key_prefix}_vt")
            
        with cols[1]:
            minutes = st.number_input("Last - Min", min_value=0, value=0, help="Enter minutes to see videos published in that timeframe", key=f"{key_prefix}_min")
            
        with cols[2]:
            all_channels = ["All"]
            if os.path.exists(VIDEO_DATA_FILE):
                try:
                    with open(VIDEO_DATA_FILE, "r", encoding="utf-8") as f:
                        d = json.load(f)
                        all_channels += sorted(list(set(v["channel_name"] for v in d.get("videos", []))))
                except:
                    pass
            channel = st.selectbox("Channel", all_channels, key=f"{key_prefix}_channel")
            
        # Row 2 for Date Range
        dr_col = st.columns(1)[0]
        with dr_col:
            today = datetime.date.today()
            date_range = st.date_input(
                "Date Range",
                value=(today, today),
                key=f"{key_prefix}_date_range"
            )
            
    return vt, minutes, channel, date_range


with st.sidebar:
    st.markdown("# 🎯 YT Recommender")
    st.caption("AI-Powered YouTube Recommendations")
    
    # Show Data Coverage Warning
    if not engine:
        st.warning("⚠️ No data loaded yet.")
    elif engine and engine.fetched_at:
        try:
            from datetime import datetime, timezone
            dt_utc = datetime.fromisoformat(engine.fetched_at.replace("Z", "+00:00"))
            now_utc = datetime.now(timezone.utc)
            diff = now_utc - dt_utc
            
            # Create a "Time Ago" string
            seconds = diff.total_seconds()
            if seconds < 60:
                time_str = "Just now"
            elif seconds < 3600:
                time_str = f"{int(seconds // 60)} mins ago"
            elif seconds < 86400:
                time_str = f"{int(seconds // 3600)} hrs ago"
            else:
                time_str = f"{int(seconds // 86400)} days ago"

            # Check if we are currently fetching (based on session state)
            if st.session_state.get('fetching_now', False):
                st.markdown(f"""
                    <div style="font-size: 0.75rem; color: #FFA500; background: rgba(255, 165, 0, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255, 165, 0, 0.2); font-weight: 600;">
                        🔄 Fetching latest news...
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="font-size: 0.75rem; color: #2BD2FF; background: rgba(43, 210, 255, 0.1); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(43, 210, 255, 0.2); font-weight: 600;">
                        💾 Updated {time_str}
                    </div>
                """, unsafe_allow_html=True)
        except Exception:
            st.info(f"💾 Refresh: {engine.fetched_at[:16]}")

    st.divider()

    page = st.radio(
        "Navigate",
        [PAGE_DASHBOARD, PAGE_TRENDING, PAGE_SEARCH, PAGE_COVERAGE, PAGE_DATA, PAGE_RECENT],
        label_visibility="collapsed",
    )

    st.divider()

    import time
    if st.button("🚀 Fetch Fresh Data", use_container_width=True, type="primary"):
        last_fetch = st.session_state.get('last_fetch_time', 0)
        if time.time() - last_fetch < 50:
            st.toast(f"Next refresh available in {int(50 - (time.time() - last_fetch))}s", icon="⏳")
        else:
            st.session_state.fetching_now = True
            st.rerun()

    st.divider()
    if st.button("🔓 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# --- TRIGGER ACTUAL FETCH IF STATE IS SET ---
if st.session_state.get('fetching_now', False):
    with st.status("Fetching latest data...", expanded=True) as status:
        st.write("Analyzing YouTube Content & Competitor Strategy...")
        try:
            videos = cached_fetch_data()
            st.write(f"Successfully fetched {len(videos)} videos!")
            import time
            st.session_state.last_fetch_time = time.time()
            st.cache_resource.clear()
            st.session_state.fetching_now = False
            status.update(label="Fetch Complete!", state="complete", expanded=False)
            st.rerun()
        except Exception as exc:
            st.session_state.fetching_now = False
            st.error(f"Could not fetch data: {exc}")
            status.update(label="Fetch Failed", state="error")
    
    with st.sidebar.expander("📖 Metrics Glossary", expanded=False):
        st.markdown("""
        **VPH (Velocity)**
        `Views / Age` - Speed of growth.
        
        **Engagement %**
        `Likes+Comments / Views`
        
        **Trend Score**
        Hybrid of Velocity (60%) and Engagement (40%).
        
        **Coverage Gap**
        Time delay behind the first reporting channel.
        """)
    




if engine is None:
    st.markdown(
        """
    <div style="text-align:center; padding:80px 20px;">
        <h1 style="font-size:3rem; margin-bottom:16px;">📊</h1>
        <h2 style="color: #FF3D71;">No Data Found</h2>
        <p style="color:#9898b0; margin-top:8px; font-size: 1.2rem;">
            It looks like there's no data available yet. <br>
            <strong>Kindly refresh the data first</strong> using the button in the sidebar to populate the dashboard.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.stop() # Prevent further execution if data is missing


if page == PAGE_DASHBOARD:
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Overview of your YouTube analytics</div>',
        unsafe_allow_html=True,
    )

    local_date_range, _, local_vt, local_cat = get_local_filters("dash")


    st.markdown("---")

    # ── FULL WIDTH TRENDING with Tabs ──────────────────────────────────────────
    st.markdown("### 🔥 Top Viral Trends (Top 50)")
    
    # Pre-filter for tabs
    df_raw = pd.DataFrame(engine.videos)
    df_raw['pub_dt'] = pd.to_datetime(df_raw['published_at'])
    df_filtered = df_raw.copy()
    if local_vt != "All":
        df_filtered = df_filtered[df_filtered["video_type"].fillna("Video") == local_vt]
    if local_date_range and len(local_date_range) == 2:
        df_filtered = df_filtered[(df_filtered["pub_dt"].dt.date >= local_date_range[0]) & (df_filtered["pub_dt"].dt.date <= local_date_range[1])]
    if local_cat != "All":
        df_filtered = df_filtered[df_filtered["channel_tag"].fillna("General") == local_cat]

    
    all_channels = sorted(df_filtered["channel_name"].unique().tolist())
    tab_names = [f"All Sources ({len(df_filtered)})"]
    for ch in all_channels:
        ch_count = len(df_filtered[df_filtered["channel_name"] == ch])
        tab_names.append(f"{ch} ({ch_count})")
        
    tabs = st.tabs(tab_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            current_ch = "All" if i == 0 else all_channels[i-1]
            trending = get_cached_trending(engine, 50, current_ch, local_date_range, "trend_score", local_vt, local_cat)

            
            if trending:
                tcols = st.columns(3)
                for index, video in enumerate(trending, start=1):
                    with tcols[(index-1) % 3]:
                        badge_text = f"#{index} Viral | 💎 {video.get('trend_score', 0):.2f} | {format_number(video.get('views_per_hour', 0))} VPH"
                        st.markdown(render_video_card(video, "trend", badge_text, show_eng_rate=True), unsafe_allow_html=True)
                        st.markdown("")
            else:
                st.info(f"No trending data available for {current_ch} matching current filters.")

elif page == PAGE_TRENDING:
    st.markdown('<div class="section-title">Trending Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Videos gaining the most traction right now</div>',
        unsafe_allow_html=True,
    )

    local_date_range, _, local_vt, local_cat = get_local_filters("trend")


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

    # Pre-filter for tabs
    df_raw = pd.DataFrame(engine.videos)
    df_raw['pub_dt'] = pd.to_datetime(df_raw['published_at'])
    df_filtered = df_raw.copy()
    if local_vt != "All":
        df_filtered = df_filtered[df_filtered["video_type"].fillna("Video") == local_vt]
    if local_date_range and len(local_date_range) == 2:
        df_filtered = df_filtered[(df_filtered["pub_dt"].dt.date >= local_date_range[0]) & (df_filtered["pub_dt"].dt.date <= local_date_range[1])]
    if local_cat != "All":
        df_filtered = df_filtered[df_filtered["channel_tag"].fillna("General") == local_cat]

    
    all_channels = sorted(df_filtered["channel_name"].unique().tolist())
    tab_names = [f"All Sources ({len(df_filtered)})"]
    for ch in all_channels:
        ch_count = len(df_filtered[df_filtered["channel_name"] == ch])
        tab_names.append(f"{ch} ({ch_count})")
        
    tabs = st.tabs(tab_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            current_ch = "All" if i == 0 else all_channels[i-1]
            trending = get_cached_trending(
                engine,
                limit, 
                channel=current_ch, 
                date_range=local_date_range, 
                sort_by=sort_key, 
                video_type=local_vt,
                category=local_cat
            )


            if trending:
                cols = st.columns(3)
                for index, video in enumerate(trending, start=1):
                    with cols[(index - 1) % 3]:
                        score = video.get('trend_score', 0)
                        vph = format_number(video.get('views_per_hour', 0))
                        
                        if sort_key == "view_count":
                            badge_text = f"#{index} Views | 👁️ {format_number(video.get('view_count', 0))}"
                        elif sort_key == "like_count":
                            badge_text = f"#{index} Likes | 👍 {format_number(video.get('like_count', 0))}"
                        elif sort_key == "comment_count":
                            badge_text = f"#{index} Comments | 💬 {format_number(video.get('comment_count', 0))}"
                        elif sort_key == "engagement_score":
                            badge_text = f"#{index} Engagement | 📈 {video.get('engagement_rate', 0):.2f}%"
                        elif sort_key == "age_hours":
                            badge_text = f"#{index} Newest"
                        elif sort_key == "views_per_hour":
                            badge_text = f"#{index} Velocity | 🚀 {vph} VPH"
                        else:
                            badge_text = f"#{index} Trending | 💎 {score:.2f} | {vph} VPH"
                            
                        st.markdown(render_video_card(video, "trend", badge_text, show_eng_rate=True), unsafe_allow_html=True)
                        st.markdown("")
            else:
                st.info(f"No trending data available for {current_ch} matching current filters.")




elif page == PAGE_SEARCH:
    st.markdown('<div class="section-title">Search Videos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Find videos across all channels using AI-powered search</div>',
        unsafe_allow_html=True,
    )

    local_date_range, _, local_vt, local_cat = get_local_filters("search")


    query = st.text_input("Search query", placeholder="Type keywords...", key="search_q")

    if query:
        # Pre-filter for tabs logic (to get channels for search results)
        raw_results = get_cached_search(engine, query, top_n=100, channel="All", date_range=local_date_range, video_type=local_vt, category=local_cat)

        
        if not raw_results:
            st.warning(f'No results found for "{query}"')
        else:
            all_channels = sorted(list(set(v["channel_name"] for v in raw_results)))
            tab_names = [f"All Sources ({len(raw_results)})"]
            for ch in all_channels:
                ch_count = sum(1 for v in raw_results if v["channel_name"] == ch)
                tab_names.append(f"{ch} ({ch_count})")
                
            tabs = st.tabs(tab_names)
            
            for i, tab in enumerate(tabs):
                with tab:
                    current_ch = "All" if i == 0 else all_channels[i-1]
                    if current_ch == "All":
                        display_results = raw_results[:24]
                    else:
                        display_results = [v for v in raw_results if v["channel_name"] == current_ch][:24]
                    
                    if display_results:
                        st.success(f'Found {len(display_results)} results for "{query}"')
                        cols = st.columns(3)
                        for index, video in enumerate(display_results):
                            with cols[index % 3]:
                                match = video.get("search_score", 0)
                                st.markdown(
                                    render_video_card(video, "match", f"Match: {match:.0%}"),
                                    unsafe_allow_html=True,
                                )
                                st.markdown("")
                    else:
                        st.info(f"No results for {current_ch} matching current query/filters.")
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

    local_date_range, _, local_vt, local_cat = get_local_filters("raw_data")


    # ── Vectorized Data Processing ──────────────────────────
    import pandas as pd
    import datetime
    df_raw = pd.DataFrame(engine.videos)
    
    if df_raw.empty:
        st.info("No data available to display.")
    else:
        df_raw['pub_dt'] = pd.to_datetime(df_raw['published_at'])
        
        # Apply Date and Type Filters First
        df_filtered = df_raw.copy()
        if local_vt != "All":
            df_filtered = df_filtered[df_filtered["video_type"].fillna("Video") == local_vt]
            
        if local_date_range and len(local_date_range) == 2:
            df_filtered = df_filtered[(df_filtered["pub_dt"].dt.date >= local_date_range[0]) & (df_filtered["pub_dt"].dt.date <= local_date_range[1])]

        if local_cat != "All":
            df_filtered = df_filtered[df_filtered["channel_tag"].fillna("General") == local_cat]


        # ── Calculate Tab Counts ────────────────────────────────
        all_channels = sorted(df_filtered["channel_name"].unique().tolist())
        
        tab_names = [f"All Sources ({len(df_filtered)})"]
        for ch in all_channels:
            ch_count = len(df_filtered[df_filtered["channel_name"] == ch])
            tab_names.append(f"{ch} ({ch_count})")
            
        tabs = st.tabs(tab_names)
        
        for i, tab in enumerate(tabs):
            with tab:
                if i == 0:
                    df_display_source = df_filtered.copy()
                    current_ch = "All"
                else:
                    current_ch = all_channels[i-1]
                    df_display_source = df_filtered[df_filtered["channel_name"] == current_ch].copy()
                
                if df_display_source.empty:
                    st.info(f"No videos found for {current_ch} matching the current filters.")
                else:
                    # Sort source data by publication datetime (most recent first)
                    df_display_source = df_display_source.sort_values("pub_dt", ascending=False)

                    # Create display dataframe
                    display_df = pd.DataFrame()
                    display_df["Published"] = df_display_source["pub_dt"].dt.strftime("%Y-%m-%d")
                    display_df["Time"] = df_display_source["pub_dt"].dt.strftime("%I:%M %p")
                    display_df["Channel"] = df_display_source["channel_name"]
                    display_df["Title"] = df_display_source["title"]
                    display_df["Type"] = df_display_source["video_type"].fillna("Video")
                    display_df["Views"] = df_display_source["view_count"]
                    display_df["Velocity (VPH)"] = df_display_source["views_per_hour"]
                    display_df["Likes"] = df_display_source["like_count"]
                    display_df["Comments"] = df_display_source["comment_count"]
                    display_df["Eng. Rate (%)"] = df_display_source["engagement_rate"].round(2)
                    display_df["Eng. Score"] = df_display_source["engagement_score"].round(4)
                    display_df["Freshness"] = df_display_source["freshness_score"].round(4)
                    display_df["Trend Score"] = df_display_source["trend_score"].round(4)
                    display_df["Duration"] = df_display_source["duration_formatted"]
                    display_df["Tags"] = df_display_source["tags"].apply(lambda x: ", ".join(x[:5]) if isinstance(x, list) else "")
                    display_df["URL"] = df_display_source["url"]

                    st.dataframe(
                        display_df,
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

                    # Download CSV for this specific tab
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label=f"📥 Download {current_ch} Data (CSV)",
                        data=csv,
                        file_name=f"youtube_data_{current_ch}_{datetime.date.today()}.csv",
                        mime='text/csv',
                        key=f"download_{current_ch}_{i}"
                    )

# End of PAGE_DATA logic

elif page == PAGE_COVERAGE:
    import re
    from collections import defaultdict
    from datetime import datetime as dt

    st.markdown('<div class="section-title">🏁 Coverage Race</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Identify which channels broke a story first — and by how many minutes</div>',
        unsafe_allow_html=True,
    )

    local_date_range, local_channel, local_vt, local_cat = get_local_filters("coverage")


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
            
            if local_cat != "All" and v.get("channel_tag", "General") != local_cat:
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
                    "Views (First Video)": v.get("view_count", 0),
                    "Likes": v.get("like_count", 0),
                    "Comments": v.get("comment_count", 0),
                    "Eng. Rate (%)": round(v.get('engagement_rate', 0), 2),
                    "Eng. Score": round(v.get('engagement_score', 0), 4),
                    "Velocity (VPH)": round(v.get('views_per_hour', 0), 1),
                    "Trend Score": round(v.get('trend_score', 0), 4),
                    "Freshness": round(v.get('freshness_score', 0), 4),
                    "Video Type": v.get("video_type", "Video"),
                    "Title (First Video)": v.get("title", ""),
                    "Video Link": v.get("url", ""),
                })

            st.dataframe(
                timeline_rows, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Views (First Video)": st.column_config.NumberColumn(format="%d"),
                    "Likes": st.column_config.NumberColumn(format="%d"),
                    "Comments": st.column_config.NumberColumn(format="%d"),
                    "Eng. Rate (%)": st.column_config.ProgressColumn(format="%.2f%%", min_value=0, max_value=20),
                    "Eng. Score": st.column_config.NumberColumn(format="%.4f"),
                    "Trend Score": st.column_config.NumberColumn(format="%.4f"),
                    "Freshness": st.column_config.NumberColumn(format="%.4f"),
                    "Velocity (VPH)": st.column_config.NumberColumn(format="%.1f"),
                    "Video Link": st.column_config.LinkColumn("Watch", display_text="Open")
                }
            )

            st.markdown("---")

            # ── ALL MATCHING VIDEOS (chronological feed table) ─────────
            st.markdown(f"### 📺 Chronological Feed")

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
                    "Published At": ts.strftime("%Y-%m-%d %H:%M") if ts else "",
                    "Type": v.get("video_type", "Video"),
                    "Views": v.get("view_count", 0),
                    "Velocity (VPH)": round(v.get("views_per_hour", 0), 1),
                    "Likes": v.get("like_count", 0),
                    "Comments": v.get("comment_count", 0),
                    "Eng. Rate (%)": round(v.get("engagement_rate", 0), 2),
                    "Duration": v.get("duration_formatted", ""),
                    "Title": v.get("title", ""),
                    "Video Link": v.get("url", ""),
                })

            st.dataframe(
                feed_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Video Link": st.column_config.LinkColumn("Watch", display_text="Open YouTube"),
                    "Views": st.column_config.NumberColumn(format="%d"),
                    "Velocity (VPH)": st.column_config.NumberColumn(format="%.1f"),
                    "Likes": st.column_config.NumberColumn(format="%d"),
                    "Comments": st.column_config.NumberColumn(format="%d"),
                    "Eng. Rate (%)": st.column_config.ProgressColumn(format="%.2f%%", min_value=0, max_value=20),
                    "Time Gap": st.column_config.TextColumn("Gap", width="small")
                }
            )

elif page == PAGE_RECENT:
    st.markdown('<div class="section-title">⏱ Recent News</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle"> The latest videos across all channels filtered by time</div>',
        unsafe_allow_html=True,
    )

    local_vt, local_minutes, local_channel, local_date_range = get_recent_filters("recent_news_grid")
    
    if local_minutes == 0:
        st.info("💡 Please enter a value in **Last - Min** above to view the latest news.")
        st.stop()

    # Filter data
    from datetime import datetime, timezone, timedelta
    
    # Base timeframe filter
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=local_minutes)
    
    # Date Range Filter setup
    start_date = None
    end_date = None
    if isinstance(local_date_range, (list, tuple)) and len(local_date_range) == 2:
        start_date, end_date = local_date_range
    elif isinstance(local_date_range, datetime.date):
        start_date = end_date = local_date_range

    filtered_vids = []
    for v in engine.videos:
        try:
            pub_dt = datetime.fromisoformat(v["published_at"].replace("Z", "+00:00"))
            
            # 1. Date Range Check
            if start_date:
                v_date = pub_dt.date()
                if v_date < start_date or v_date > end_date:
                    continue
            
            # 2. Timeframe (Minutes) Check
            if pub_dt < cutoff:
                continue
                
            # 3. Video Type Filter
            if local_vt != "All" and v.get("video_type", "Video") != local_vt:
                continue
                
            # 4. Channel Filter (Ignored to allow tabs to show all channels)
            
            v_copy = v.copy()
            v_copy["live_age"] = (now - pub_dt).total_seconds()
            filtered_vids.append(v_copy)
        except:
            continue

    # Sort by live age (smallest first = newest)
    filtered_vids.sort(key=lambda x: x.get("live_age", 999999))
    
    # ── Source Tabs Logic ───────────────────────────────────
    all_channels_in_data = sorted(list(set(v.get("channel_name") for v in filtered_vids)))
    tab_names = [f"All Sources ({len(filtered_vids)})"]
    for ch in all_channels_in_data:
        ch_count = sum(1 for v in filtered_vids if v.get("channel_name") == ch)
        tab_names.append(f"{ch} ({ch_count})")
        
    tabs = st.tabs(tab_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            if i == 0:
                display_vids = filtered_vids
            else:
                ch_name = all_channels_in_data[i-1]
                display_vids = [v for v in filtered_vids if v.get("channel_name") == ch_name]
                
            if not display_vids:
                st.info("No videos found for this source.")
            else:
                st.success(f"Showing all {len(display_vids)} latest videos.")
                cols = st.columns(3)
                for index, video in enumerate(display_vids, start=1):
                    with cols[(index - 1) % 3]:
                        badge_text = f"#{index} Newest | {time_ago(video.get('published_at', ''))}"
                        st.markdown(render_video_card(video, "trend", badge_text, show_eng_rate=True), unsafe_allow_html=True)
                        st.markdown("")
