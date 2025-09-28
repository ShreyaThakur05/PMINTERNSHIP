@echo off
echo Starting AI-Powered Internship Allocation System...
echo.

echo Step 1: Generating sample data...
python datasetcode.py

echo.
echo Step 2: Starting API server...
start "API Server" python app.py

echo.
echo Step 3: Opening frontend...
timeout /t 3 /nobreak >nul
start frontend.html

echo.
echo System started successfully!
echo - API Server: http://localhost:5000
echo - Frontend: frontend.html (opened in browser)
echo.
echo Next steps:
echo 1. Update .env file with your MongoDB Atlas connection string
echo 2. Click 'Load Data from CSV' in the frontend
echo 3. Click 'Run Allocation' to see the AI allocation in action
echo.
pause