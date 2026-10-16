# FraudGuard AI Analytics Dashboard

A Streamlit-based analytics dashboard for the fraud detection system.

## 🎯 Features

- **Overview Page**: Model performance metrics and feature information
- **Live Prediction**: Real-time transaction analysis using trained models
- **Model Performance**: Detailed metrics from evaluation reports
- **Transaction Data**: Sample data reference with filtering

## 🚀 How to Run

### Option 1: Command Line

```bash
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\streamlit run dashboard/app.py
```

### Option 2: Using Batch File

Double-click: `start-dashboard.bat` (in project root)

### Option 3: Using PowerShell

```powershell
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\streamlit run dashboard/app.py
```

## 📋 Requirements

- Python 3.9+
- streamlit
- plotly
- pandas
- numpy
- scikit-learn
- joblib

All dependencies are already installed in the project's virtual environment.

## 🎨 Pages

### 1. Overview
- Model performance comparison
- Feature lists for both models
- Accuracy metrics

### 2. Live Prediction
- Transaction input form
- Real-time fraud detection
- Results with probability scores
- Feature analysis

### 3. Model Performance
- Detailed metrics from CSV reports
- Data drift monitoring
- Confusion matrix metrics

### 4. Transaction Data
- Sample transaction data
- Filtering options
- CSV download

## 🔗 Integration

The dashboard uses the same:
- Trained models from `models/production/`
- Feature engineering from `backend/features.py`
- Performance reports from `mlops/monitoring/reports/`

## 📊 Model Information

- **Pre-Approval Model**: 99.92% accuracy, 6 features
- **Post-Processing Model**: 99.99% accuracy, 12 features

## ⚠️ Notes

- This is an analytics dashboard, not a replacement for the production API
- Uses the same models as the FastAPI backend
- Ideal for monitoring, analytics, and internal use
- The production frontend (HTML/CSS/JS) is better for customer-facing applications

## 🔄 Running Alongside Main System

You can run both:
- **FastAPI Backend**: Port 8000
- **HTML Frontend**: Port 3000
- **Streamlit Dashboard**: Port 8501 (default)

All three can run simultaneously without conflicts.
