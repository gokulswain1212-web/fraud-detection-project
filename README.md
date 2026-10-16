# 🛡️ FraudGuard AI - Real-Time Fraud Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Advanced machine learning models for real-time financial fraud detection**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [API Docs](#-api-documentation) • [Architecture](#-architecture)

</div>

---

## 📋 Overview

FraudGuard AI is a production-ready fraud detection system that uses machine learning to analyze financial transactions in real-time. The system employs a two-stage detection approach:

- **Pre-Approval Model**: Analyzes transactions before settlement using available transaction data
- **Post-Processing Model**: Enhanced analysis after sender/receiver balances are known

With **99.9% accuracy** for pre-approval and **99.99% accuracy** for post-processing, the system provides reliable fraud detection while maintaining minimal false positives.

---

## ✨ Features

### 🤖 Machine Learning
- **Dual-Stage Detection**: Pre-approval and post-processing models
- **High Accuracy**: 99.9% - 99.99% detection accuracy
- **Real-Time Inference**: < 100ms response time
- **Feature Engineering**: Automatic derivation of transaction features

### 🌐 API
- **RESTful API**: Built with FastAPI
- **Auto Documentation**: Interactive Swagger UI
- **Input Validation**: Pydantic models for data validation
- **Error Handling**: Comprehensive error responses

### 🎨 Frontend
- **Modern UI**: AI-themed dark design with gradients
- **Real-Time Analysis**: Instant fraud detection results
- **Data Visualizations**: 8 interactive charts and plots
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Tabbed Interface**: Organized visualization categories

### 📊 Data Analysis
- **Exploratory Data Analysis**: Comprehensive notebooks
- **Visualizations**: Transaction patterns, fraud trends, correlations
- **Monitoring**: Data drift detection and model performance tracking

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Modern web browser

### Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd fraud-detection-project
```

2. **Create virtual environment**
```bash
python -m venv .venv
```

3. **Activate virtual environment**

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

5. **Verify installation**
```bash
python -m pytest tests/ -v
```

---

## ⚡ Quick Start

### Option 1: Using Startup Scripts (Recommended)

**Windows:** Double-click `start-all.bat`

This will:
- Start the backend server (port 8000)
- Start the frontend server (port 3000)
- Open your browser automatically

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\Users\LENOVO\Desktop\fraud-detection-project\frontend
python -m http.server 3000
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📁 Project Structure

```
fraud-detection-project/
├── backend/                    # FastAPI backend
│   ├── main.py                # API endpoints and server
│   ├── features.py            # Feature engineering
│   ├── schemas.py             # Pydantic models
│   └── requirements.txt       # Backend dependencies
├── frontend/                   # Web frontend
│   ├── index.html             # Main HTML structure
│   ├── styles.css             # Modern CSS styling
│   ├── app.js                 # JavaScript logic
│   ├── *.png                  # Visualization plots
│   └── README.md              # Frontend documentation
├── models/                     # Trained models
│   ├── production/            # Production models
│   │   ├── fraud_preapproval_model.pkl
│   │   └── fraud_postprocessing_model.pkl
│   └── candidates/            # Model candidates
├── notebooks/                  # Jupyter notebooks
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   ├── 05_model_evaluation.ipynb
│   └── 06_data_cleaning.ipynb
├── data/                       # Data directories
│   ├── raw/                   # Raw dataset
│   ├── processed/             # Processed data
│   └── reference/             # Reference data
├── figures/                    # EDA visualizations
│   ├── fraud_vs_legitimate.png
│   ├── fraud_by_transaction_type.png
│   ├── transaction_amount_distribution.png
│   └── ... (8 total plots)
├── mlops/                      # MLOps utilities
│   └── monitoring/
│       └── reports/           # Model performance reports
├── src/                        # Reusable ML modules
│   ├── data_processing.py     # Data loading & cleaning
│   ├── train.py               # Model training
│   ├── evaluate.py            # Model evaluation
│   ├── predict.py             # Inference logic
│   └── features.py            # Feature engineering
├── tests/                      # Test suite
│   ├── test_api.py            # API tests
│   ├── test_features.py       # Feature tests
│   └── test_data_processing.py
├── start-all.bat              # Start everything (Windows)
├── start-backend.bat          # Start backend (Windows)
├── start-frontend.bat         # Start frontend (Windows)
├── QUICKSTART.md              # Quick start guide
└── README.md                  # This file
```

---

## 🎯 Model Performance

### Pre-Approval Model
- **Accuracy**: 99.92%
- **Fraud Precision**: 77.79%
- **Fraud Recall**: 54.35%
- **Fraud F1-Score**: 63.99%
- **Features**: 6 (Step, Type, Amount, Old Balance Org/Dest, Sender Balance Zero)

### Post-Processing Model
- **Accuracy**: 99.99%
- **Fraud Precision**: 100%
- **Fraud Recall**: 99.33%
- **Fraud F1-Score**: 99.66%
- **Features**: 12 (includes balance changes and mismatches)

### Model Metrics

| Metric | Pre-Approval | Post-Processing |
|--------|--------------|------------------|
| True Negatives | 1,270,626 | 1,270,881 |
| False Positives | 255 | 0 |
| False Negatives | 750 | 11 |
| True Positives | 893 | 1,632 |

---

## 🔌 API Documentation

### Endpoints

#### `GET /`
Health check endpoint

**Response:**
```json
{
  "message": "Fraud Detection API is running!"
}
```

#### `GET /health`
System health check with model status

**Response:**
```json
{
  "status": "healthy",
  "preapproval_model_loaded": true,
  "postprocessing_model_loaded": true
}
```

#### `POST /predict`
Pre-approval fraud detection

**Request Body:**
```json
{
  "Step": 1,
  "Type": "PAYMENT",
  "Amount": 9839.64,
  "Oldbalanceorg": 170136.0,
  "Oldbalancedest": 0.0
}
```

**Response:**
```json
{
  "model": "fraud_preapproval",
  "prediction": 0,
  "result": "Likely Legitimate",
  "fraud_probability": 0.0,
  "features_used": ["Step", "Type", "Amount", "Oldbalanceorg", "Oldbalancedest", "SenderBalanceZero"],
  "warning": "This is a model prediction, not a confirmed fraud finding."
}
```

#### `POST /predict/post-processing`
Post-processing fraud detection (requires new balances)

**Request Body:**
```json
{
  "Step": 1,
  "Type": "PAYMENT",
  "Amount": 9839.64,
  "Oldbalanceorg": 170136.0,
  "Oldbalancedest": 0.0,
  "Newbalanceorig": 160296.36,
  "Newbalancedest": 0.0
}
```

**Response:**
```json
{
  "model": "fraud_postprocessing",
  "prediction": 0,
  "result": "Likely Legitimate",
  "fraud_probability": 0.0,
  "features_used": ["Step", "Type", "Amount", "Oldbalanceorg", "Newbalanceorig", "Oldbalancedest", "Newbalancedest", "SenderBalanceChange", "SenderBalanceMismatch", "ReceiverBalanceChange", "ReceiverBalanceMismatch", "SenderBalanceZero"],
  "warning": "This is a model prediction, not a confirmed fraud finding."
}
```

### Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation with Swagger UI.

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────┐
│   Frontend      │
│  (React/HTML)   │
└────────┬────────┘
         │ HTTP
         ↓
┌─────────────────┐
│   Backend API   │
│   (FastAPI)     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Feature Engine │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  ML Models      │
│  (Scikit-learn) │
└─────────────────┘
```

### Data Flow

1. **User Input**: Transaction data entered in frontend
2. **API Request**: Data sent to FastAPI backend
3. **Feature Engineering**: Automatic derivation of features
4. **Model Inference**: Prediction from trained model
5. **Response**: Results returned to frontend with probability
6. **Visualization**: Results displayed with metrics and charts

---

## 🛠️ Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Scikit-learn**: Machine learning library
- **Pandas**: Data manipulation and analysis
- **Joblib**: Model serialization
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Vanilla JavaScript**: No framework dependencies
- **Inter Font**: Clean typography
- **Responsive Design**: Mobile-first approach

### Data Science
- **Jupyter Notebooks**: Interactive development
- **Matplotlib/Seaborn**: Data visualization
- **NumPy**: Numerical computing

### Testing
- **Pytest**: Testing framework
- **FastAPI TestClient**: API testing

---

## 📊 Visualizations

The frontend includes 8 interactive visualizations:

### Overview Tab
- Fraud vs Legitimate Transactions
- Fraud Distribution by Transaction Type

### Transactions Tab
- Transaction Amount Distribution
- Transaction Amount by Fraud Status

### Analysis Tab
- Fraud Rate by Transaction Type
- Fraud Transactions Over Time
- Fraud vs Legitimate Over Time
- Feature Correlation Heatmap

---

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

### Test Coverage
- API endpoint tests
- Feature engineering tests
- Input validation tests
- Model loading tests

---

## 📈 MLOps

### Monitoring
- Data drift detection
- Model performance tracking
- Feature distribution monitoring

### Reports
Model performance reports are generated in `mlops/monitoring/reports/`:
- `fraud_preapproval_report.csv`
- `fraud_postprocessing_report.csv`
- `data_drift_report.csv`

---

## 🔒 Security Considerations

⚠️ **Important:**
- This is a model prediction, not a confirmed fraud finding
- Always verify with additional checks before taking action
- Do not use as the sole decision-making tool
- Implement proper authentication for production use
- Add rate limiting to prevent abuse
- Log all predictions for audit trails

---

## 🚧 Future Enhancements

- [ ] Authentication & Authorization
- [ ] Transaction history dashboard
- [ ] Real-time monitoring stream
- [ ] Advanced analytics dashboard
- [ ] Export results to CSV/PDF
- [ ] Multi-language support
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Model retraining pipeline
- [ ] A/B testing framework

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the project maintainers.

---

## 🙏 Acknowledgments

- PaySim dataset for synthetic financial transaction data
- Scikit-learn community for excellent ML tools
- FastAPI team for the amazing web framework

---

<div align="center">

**Built with ❤️ for fraud detection**

[⬆ Back to Top](#-fraudguard-ai---real-time-fraud-detection-system)

</div>
