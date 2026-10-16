# FraudGuard AI Business Intelligence Dashboard

A professional BI-style dashboard built with Plotly Dash, designed to look like Power BI/Tableau for executive reporting and analytics.

## 🎯 Features

### Executive KPI Cards
- Total Transactions
- Fraud Cases
- Total Amount Processed
- Model Accuracy

### Interactive Filters
- Transaction Type Filter
- Amount Range Slider
- Hour of Day Range
- Fraud-Only Toggle

### Professional Charts
- **Fraud Trends Over Time** - Line chart showing fraud cases over time
- **Fraud by Transaction Type** - Pie chart distribution
- **Amount Distribution** - Histogram colored by fraud status
- **Fraud by Hour of Day** - Line chart showing hourly patterns

### Model Performance Comparison
- Pre-Approval Model metrics (Accuracy, Precision, Recall, F1-Score)
- Post-Processing Model metrics (Accuracy, Precision, Recall, F1-Score)
- Visual progress bars for each metric

### Data Table
- Interactive data table with 100 records
- Color-coded fraud rows (red highlight)
- Pagination support
- Scrollable for large datasets

## 🚀 How to Run

### Option 1: Batch File (Easiest)
Double-click: `start-bi-dashboard.bat`

### Option 2: Command Line
```bash
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\python.exe bi-dashboard\app.py
```

### Option 3: PowerShell
```powershell
cd C:\Users\LENOVO\Desktop\fraud-detection-project
.venv\Scripts\python.exe bi-dashboard\app.py
```

## 🌐 Access

The dashboard runs on: **http://localhost:8050**

## 📋 Requirements

- Python 3.9+
- dash
- dash-bootstrap-components
- plotly
- pandas
- numpy

All dependencies are already installed in the project's virtual environment.

## 🎨 Design Features

- **Dark Theme**: Professional dark theme (Cyborg Bootstrap)
- **Responsive Layout**: Works on desktop and tablet
- **Interactive Charts**: All charts are interactive (zoom, pan, hover)
- **Real-time Filtering**: Filters update all charts instantly
- **Color Coding**: Fraud cases highlighted in red
- **Professional Styling**: Business-grade design suitable for executives

## 📊 Data Source

Currently uses sample data for demonstration. To connect to real data:

1. Replace the `generate_sample_data()` function with data loading from your database
2. Connect to your actual transaction database
3. Update the metrics to load from `mlops/monitoring/reports/`

## 🔧 Customization

### Change Theme
Edit line 21 in `app.py`:
```python
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
```
Available themes: BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNALLY, LUX, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SOLAR, SPACELAB, SUPERHERO, UNITED, YETI

### Change Port
Edit line 354 in `app.py`:
```python
app.run(debug=True, port=8050)  # Change 8050 to your preferred port
```

## 🔄 Running Alongside Other Systems

You can run all four systems simultaneously:
- **FastAPI Backend**: Port 8000
- **HTML Frontend**: Port 3000
- **Streamlit Dashboard**: Port 8501
- **BI Dashboard**: Port 8050

No conflicts between ports!

## 📈 Comparison with Other Dashboards

| Dashboard | Purpose | Users | Best For |
|------------|---------|-------|----------|
| **HTML Frontend** | Transaction analysis | End users | Customer-facing |
| **Streamlit Dashboard** | Analytics & monitoring | Data scientists | Quick analysis |
| **BI Dashboard** | Executive reporting | Executives/Managers | Business decisions |

## 🎯 Use Cases

- **Executive Reporting**: High-level metrics for stakeholders
- **Business Intelligence**: Trend analysis and patterns
- **Performance Monitoring**: Track model performance over time
- **Data Exploration**: Interactive filtering and drill-down
- **Presentations**: Professional charts for meetings

## ⚠️ Notes

- Currently uses sample data for demonstration
- In production, connect to your database
- Dashboard refreshes with page reload (not real-time)
- Ideal for periodic reporting and analysis

## 📝 Future Enhancements

- Connect to real database
- Add real-time updates
- Export to PDF/Excel
- Add more chart types
- Drill-down capabilities
- Alert system
- User authentication
