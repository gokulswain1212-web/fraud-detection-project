# Quick Start Guide

## 🚀 Easy Startup Scripts

I've created batch files to make it easy to start your fraud detection application.

### Option 1: Start Everything (Recommended)

**Double-click:** `start-all.bat`

This will:
- Start the backend server
- Start the frontend server
- Open your browser to http://localhost:3000
- Open two command windows (keep them open!)

### Option 2: Start Individually

**Backend:** Double-click `start-backend.bat`
**Frontend:** Double-click `start-frontend.bat`

Then open your browser to: http://localhost:3000

---

## 📂 File Locations

All scripts are in the project root:
```
C:\Users\LENOVO\Desktop\fraud-detection-project\
├── start-all.bat          ⭐ Start everything (recommended)
├── start-backend.bat      Start backend only
├── start-frontend.bat     Start frontend only
└── README.md              Project documentation
```

---

## 💡 How to Use

1. **Double-click** `start-all.bat`
2. **Wait** 3-5 seconds for servers to start
3. **Browser opens** automatically to http://localhost:3000
4. **Keep both command windows open** while using the app
5. **Close windows** when you're done (press Ctrl+C or close the window)

---

## 🌐 Access Points

| What | URL |
|------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |

---

## ⚠️ Important Notes

- **Both command windows must stay open** while using the application
- If you close a window, that server stops working
- The backend must be running for the frontend to work
- If something doesn't work, close all windows and try again

---

## 🔧 Troubleshooting

**Backend won't start?**
- Make sure Python is installed
- Check that the virtual environment exists at `.venv\`
- Try running: `.venv\Scripts\python.exe -m pip install -r backend\requirements.txt`

**Frontend won't start?**
- Make sure Python is installed
- Try a different port: `python -m http.server 3001`
- Then access at: http://localhost:3001

**Can't access localhost?**
- Check your firewall settings
- Try using: http://127.0.0.1:3000 instead

---

## 📝 What Each Script Does

### `start-all.bat`
- Opens backend in one window
- Opens frontend in another window
- Opens your browser automatically
- **Easiest option - just double-click!**

### `start-backend.bat`
- Starts only the FastAPI backend
- Useful if you want to test the API alone
- Access at http://localhost:8000/docs

### `start-frontend.bat`
- Starts only the frontend web server
- Useful if backend is already running
- Access at http://localhost:3000

---

## 🎯 Next Steps

Once the application is running:
1. Fill in the transaction form
2. Click "Analyze Transaction"
3. See real-time fraud detection results
4. Try different transaction types and amounts

Have fun with your fraud detection system! 🎉
