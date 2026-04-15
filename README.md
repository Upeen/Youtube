# 🎯 YouTube Recommendation System

An AI-powered YouTube video recommendation engine featuring a comprehensive, interactive **Streamlit** dashboard. Get real-time data from top news channels and intelligent recommendations leveraging **TF-IDF content-based filtering** and **log-scaled engagement scoring**.

## ✨ Features

- **🔥 Trending Analysis:** Pinpoint rapidly growing videos based on velocity (views per hour) and comprehensive engagement metrics.
- **⭐ Smart Recommendations:** Content-based filtering tailored using TF-IDF text vectorization across titles, descriptions, and tags.
- **🔗 Content Matching:** Find closely related videos with advanced cosine-similarity.
- **🔍 Global Search:** AI-enhanced full-text search across all collected metadata.
- **📺 Channel Deep-dive:** Track performance overview per channel, calculating channel-wide engagement rates, views, and subscriber milestones.
- **🎨 Premium UI:** Custom-styled dark Streamlit theme with glassmorphism elements, CSS gradients, dynamic UI cards, and responsive layout.

## 📁 System Architecture

```text
youtube-recommendation-system_new/
├── app.py              # Main Streamlit web dashboard application
├── fetch_data.py       # YouTube Data API v3 integration and data extractor
├── recommender.py      # TF-IDF logic, Cosine Similarity, and Scoring Engine
├── config.py           # Core configuration (API Keys, Channel lists, Filters)
├── requirements.txt    # Python dependencies
├── start.bat           # Windows startup and initialization script
├── start.sh            # Linux/Mac startup and initialization script
└── data/               # Persistent local storage for JSON data files
```

## 🚀 Quick Start

### 1. Pre-requisites
- **Python 3.8+** installed on your system.
- An Active YouTube Data API v3 Key (configured in `config.py`).

### 2. Automatic Launch (Recommended)
You can start the environment using our launch scripts which handle dependency installation and give you an option to fetch fresh data.

**For Windows:**
```cmd
# Double-click start.bat or run from terminal:
start.bat
```

**For Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

### 3. Manual Launch
If you prefer running commands manually:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fetch latest data (Optional if data/videos.json already exists)
python fetch_data.py

# 3. Launch Dashboard
streamlit run app.py
```
The application will automatically open your default browser at `http://localhost:8501`.

## ⚙️ Configuration (`config.py`)

The pipeline handles multiple parameters that you can adjust within the `config.py` file:
- **`YOUTUBE_API_KEY`**: Your Google Cloud YouTube Data API Key.
- **`CHANNEL_IDS`**: Dictionary of channels you wish to track. Provide the channel name and ID.
- **`DAYS_BACK`**: The single variable responsible for the data fetch duration. Set this to 15, 30, or any number to pull videos from exactly that many days ago. The engine handles the mathematical conversion to ISO timestamps automatically.

## 📊 How the Engine Works (`recommender.py`)

The core intelligence behind the recommendations uses a robust content and performance-based hybrid approach:

1. **Text Normalization:** Extracted texts are stripped entirely of noise, custom stop-words are eliminated, and strings are cleanly tokenized.
2. **Feature Weighting:** Metadata features receive varying priorities (`Title` gets a 3x multiplier, `Tags` get 2x, `Description` gets 1x) as an inputted document sequence.
3. **TF-IDF Processing:** Calculates Term Frequency-Inverse Document Frequency sparse vectors across the whole dataset.
4. **Cosine Similarity:** Measures the normalized internal angle distances between numerical document counterparts.
5. **Score Aggregation Algorithm:** The final metrics heavily balance recency and user-action:
   - **Content Match** = 50% calculation (TF-IDF Similarity)
   - **Engagement Ratio** = 30% calculation (Log-normalized distribution of Views + Likes + Comments)
   - **Freshness Factor** = 20% calculation (Temporal decay favoring 0-6 hour old content)

## 📺 Default Monitored Channels

The system comes pre-configured to analyze top Indian news networks directly out-of-the-box:
- **Zee News**
- **Times of India**
- **News18 India**
- **Aaj Tak**
- **India TV**
- **NDTV**
- **ABP News**
