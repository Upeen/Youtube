# 🎨 Skill: UI Customization & Glassmorphism Styling

## Overview
This skill provides instructions for modifying the Streamlit dashboard's aesthetics, including custom CSS injection for glassmorphism and card layouts.

## 🛠️ Implementation Details
- **Main App**: `app.py`
- **Styling Method**: `st.markdown(..., unsafe_allow_html=True)`
- **Design System**: Dark mode, glassmorphism (`backdrop-filter`), and CSS gradients.
- **Sidebar Indicators**: Shows real-time "Last Data Refreshed" (local time) indicating the last API synchronization.

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
