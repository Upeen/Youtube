# 🎨 Skill: UI Customization & Glassmorphism Styling

## Overview
This skill provides instructions for modifying the Streamlit dashboard's aesthetics, including custom CSS injection for glassmorphism and card layouts.

## 🛠️ Implementation Details
- **Main App**: `app.py`
- **Styling Method**: `st.markdown(..., unsafe_allow_html=True)`
- **Design System**: Professional "Inter" font system, dark mode, glassmorphism (`backdrop-filter`), and CSS gradients.
- **Output Files**: `data/videos.json`, `data/videos.csv`
- **Shorts Logic**: Content is tagged as "Short" if `duration <= 60s` OR the tag `"shorts"` is present in the video metadata.
- **Typography**: Optimized information density with reduced font sizes for titles (0.8rem), channel names (0.72rem), and stats (0.68rem).
- **Animations**: Premium UX featuring `fadeInUp` card entrance, `pulse` trending badges, and interactive hover scaling.
- **Authentication**: The system requires a `private_key.json` file for authorization, validated against `project_id`.

## 🚀 Execution Instructions

### Modifying the Theme
- Locate the `<style>` block in `app.py`.
- Update the `--glass-bg` or `--accent-color` variables to change the global color scheme.

### Adding New UI Cards
- Use the `render_metric_card` function (or equivalent) in `app.py`.
- Ensure new elements have the `.glass-card` CSS class for visual consistency.

### Updating Animations
- Modify the `@keyframes` block in the CSS section to adjust entry animations or hover effects.

## ⚠️ Safety & Constraints
- **Streamlit Constraints**: Be careful with large HTML blobs that might break the Streamlit widget lifecycle.
- **Responsiveness**: Always test changes with different browser widths.

## 🔍 Validation
- Refresh the browser tab running the Streamlit app.
- Ensure transparency and blur effects (glassmorphism) are rendering correctly.
