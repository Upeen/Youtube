# YouTube Analytics Engine - Render Deployment Guide

## Overview
This guide covers the steps to deploy the **YouTube Analytics Engine** to **Render** (render.com).

---

## 🛠 Prerequisites

1.  **GitHub Account**: Push your code to a GitHub repository.
2.  **Render Account**: Sign up at [render.com](https://render.com).
3.  **YouTube API Key**: Obtain a key from the [Google Cloud Console](https://console.cloud.google.com/).

---

## 📂 Project Structure for Deployment

```text
Youtube/
├── app.py              # Main Streamlit Application
├── config.py           # Configuration (reads from environment variables)
├── fetch_data.py       # Data fetching logic
├── recommender.py      # AI Recommendation Engine
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Streamlit server configuration
├── render.yaml         # Render Blueprint (Infrastructure as Code)
├── Procfile            # Deployment process file
└── DEPLOYMENT.md       # This guide
```

---

## 🚀 Deployment Steps

### 1. Push to GitHub
If you haven't already, initialize a git repo and push your code:
```bash
git init
git add .
git commit -m "Prepare for Render deployment"
git branch -M main
git remote add origin https://github.com/yourusername/youtube-analytics-engine.git
git push -u origin main
```

### 2. Deploy on Render
1.  Log in to your **Render Dashboard**.
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository.
4.  Render will automatically detect the settings from `render.yaml`:
    *   **Name**: `youtube-recommender` (or your choice)
    *   **Environment**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `streamlit run app.py`

### 3. Configure Environment Variables
1.  In the Render dashboard, navigate to your service's **Environment** tab.
2.  Click **Add Environment Variable**.
3.  Add the following:
    *   **Key**: `YOUTUBE_API_KEY`
    *   **Value**: `YOUR_ACTUAL_API_KEY_HERE`
4.  Click **Save Changes**. Render will automatically redeploy with the new settings.

---

## ⚠️ Important Considerations

### Data Persistence (Ephemeral Disk)
*   **Free/Standard Instance**: Render uses an ephemeral filesystem. This means any data fetched using the **"Fetch Fresh Data"** button will be lost when the instance restarts or redeploys.
*   **Solutions**:
    *   **Persistent Disk**: Attach a Render Persistent Disk (requires a paid plan).
    *   **Database**: Store video data in an external database like MongoDB or PostgreSQL.
    *   **Cloud Storage**: Save `videos.json` to AWS S3 or Google Cloud Storage.

### RAM Limits
Streamlit can be memory-intensive. Ensure you are monitoring the metrics in the Render dashboard. If the app crashes with "Out of Memory", you may need to upgrade the instance size or reduce the number of channels being fetched in `config.py`.

---

## 💻 Local Development

To run the project locally:
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API Key (optional if already in config.py)
# Windows:
set YOUTUBE_API_KEY=your_key_here
# Mac/Linux:
export YOUTUBE_API_KEY=your_key_here

# 3. Start the app
streamlit run app.py
```

---

## 🛠 Troubleshooting
*   **Port Issues**: Render expects the app to bind to port `10000`. This is handled by `.streamlit/config.toml`.
*   **Import Errors**: Ensure `requirements.txt` is updated after adding new libraries.
*   **Authentication**: If you lose access, ensure your `private_key.json` (if used) is present or use the hardcoded fallback in `app.py`.
