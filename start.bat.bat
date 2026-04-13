@echo off
echo ========================================
echo   AI Hardware Debug Assistant
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)
echo OK: Python found

echo.
echo [2/3] Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)
echo OK: Dependencies ready

echo.
echo [3/3] Starting OpenCode check...
curl -s http://localhost:8080/api/tags >nul 2>&1
if errorlevel 1 (
    echo WARNING: OpenCode server not detected at http://localhost:8080
    echo Please start OpenCode with: opencode serve
    echo.
    echo Press any key to continue anyway or Ctrl+C to exit...
    pause >nul
)

echo.
echo ========================================
echo   Starting Streamlit Application...
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

streamlit run app.py --server.port 8501

pause
