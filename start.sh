#!/bin/bash

echo "============================================"
echo "  YouTube Recommendation System"
echo "============================================"
echo ""

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python is not installed or not in PATH."
    echo "Please install Python from https://python.org"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
python -m pip install -r requirements.txt --quiet
echo ""

# ALWAYS run dashboard only
echo "Starting dashboard using existing data..."
echo ""

echo "============================================"
echo "  Dashboard will open in your browser"
echo "============================================"
echo ""

python -m streamlit run app.py

read -p "Press Enter to exit..."