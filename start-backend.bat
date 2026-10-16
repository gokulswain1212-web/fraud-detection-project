@echo off
echo Starting Fraud Detection Backend...
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
pause
