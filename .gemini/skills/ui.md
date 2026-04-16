# 🎨 Skill: UI Customization & Glassmorphism Styling

## Overview
This skill provides instructions for maintaining the Streamlit dashboard's premium "True Black" aesthetics, including Glassmorphism injection, localized filtering, and high-fidelity card layouts.

## 🛠️ Implementation Details
- **Main App**: `app.py`
- **Theme**: **True Black** high-contrast mode (Background: `#050508`).
- **Styling Method**: Unified CSS injection via `st.markdown(..., unsafe_allow_html=True)`.
- **Design System**: 
  - **Typography**: 'Inter' font family with optimized weights (400 to 900). 
  - **Glassmorphism**: `backdrop-filter: blur(10px)` with semi-transparent gradients.
  - **Colors**: Viral Red (`#FF3D71`), Electric Blue (`#2BD2FF`), and Deep Indigo (`#4158D0`).
- **Control Plane**: 
  - **Localized Filters**: Each tab (Dashboard, Trending, Search, Race) has its own independent filter state (`get_local_filters`).
  - **Interactive Badges**: Real-time `pulse` animations for trending hits and `fadeInUp` entrance for all data loads.

## 🚀 Execution Instructions

### Modifying the Theme
- Locate the `<style>` block in `app.py`.
- Update the `:root` variables or CSS classes like `.stat-card` and `.video-card` to change the global color scheme or blur intensity.

### Adding New UI Modules
- Use the `render_video_card` or `render_stat_card` functions to maintain HTML structure.
- **Critical**: Ensure new inputs use a unique `key` parameter (e.g., `key=f"{prefix}_search"`) to avoid state crosstalk between tabs.

### Updating Animations
- The system uses CSS3 keyframes (`fadeInUp`, `pulse`). Modify these in the styles block to adjust the "weight" and timing of the UI transitions.

## ⚠️ Safety & Constraints
- **HTML Sanitization**: Streamlit allows HTML but some tags may be stripped. Stick to `div`, `span`, `a`, and `img`.
- **Z-Index**: Glassmorphism depends on clear layering. Avoid overlapping multiple blur layers which can degrade performance.
- **Responsive Breakpoints**: The layout uses `st.columns`. Always verify readability on both desktop and tablet views.

## 💡 Easy Understanding: UI Addition Walkthrough

**Task**: You want to add a "Last Updated" badge to each video card.

1.  **Open `app.py`** and locate the `render_video_card` function.
2.  **Add the HTML code**:
    ```html
    <div style="font-size: 0.6rem; color: #92FE9D; margin-top: 4px;">
        💾 Sync: {video.get('fetched_at', 'N/A')[:16]}
    </div>
    ```
3.  **Add CSS for specific styling** (if needed) in the main `<style>` block:
    ```css
    .sync-badge {
        background: rgba(146, 254, 157, 0.1);
        border: 1px solid rgba(146, 254, 157, 0.2);
    }
    ```
4.  **Save & Refresh**: The dashboard will automatically reflect the change with a smooth `fadeInUp` animation.

---

## 🔍 Validation
- Switch between **Dashboard** and **Trending** tabs. Ensure the "Date Range" set in one tab does NOT change the selection in the other.
- Hover over a video card; it should scale upwards significantly (`transform: translateY(-5px)`) to provide tactile feedback.
