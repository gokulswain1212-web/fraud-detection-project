@echo off
echo Starting Fraud Detection Application...
echo.
echo Backend and Frontend will open in separate windows.
echo Keep both windows open to use the application.
echo.
echo Frontend: http://localhost:3000
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
pause

start "Fraud Detection Backend" cmd /k "cd C:\Users\LENOVO\Desktop\fraud-detection-project && .venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

start "Fraud Detection Frontend" cmd /k "cd C:\Users\LENOVO\Desktop\fraud-detection-project\frontend && python -m http.server 3000"

timeout /t 2 /nobreak >nul

start http://localhost:3000

echo.
echo Application started! Two command windows should be open.
echo Close them when you're done using the application.
