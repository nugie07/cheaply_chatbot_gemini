#!/bin/bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Virtual environment tidak ditemukan!"
    echo "Jalankan setup_venv.sh terlebih dahulu."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "Starting Cheaply Restaurant Chatbot..."
streamlit run app.py

