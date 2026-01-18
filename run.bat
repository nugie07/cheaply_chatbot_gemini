@echo off
REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment tidak ditemukan!
    echo Jalankan setup_venv.bat terlebih dahulu.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo Starting Cheaply Restaurant Chatbot...
streamlit run app.py
pause

