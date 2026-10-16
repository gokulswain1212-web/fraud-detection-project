# FraudGuard AI Frontend

A modern, AI-themed frontend for the fraud detection system.

## Features

- **Modern UI Design**: Dark theme with gradient accents and glassmorphism effects
- **Real-time Analysis**: Connects to FastAPI backend for instant fraud detection
- **Dual Model Support**: Pre-approval and post-processing fraud detection
- **Visual Feedback**: Color-coded results, probability bars, and animations
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Form Validation**: Client-side validation for all transaction fields

## Design Elements

- **Color Palette**: Dark slate background with purple/indigo gradients
- **Typography**: Inter font family for clean, modern look
- **Animations**: Smooth transitions, pulse effects, and loading states
- **AI Branding**: Gradient badges, glowing effects, and futuristic aesthetics

## Running the Frontend

### Prerequisites

- Python 3.x (for backend)
- Modern web browser

### Start the Backend

```bash
cd /c/Users/LENOVO/Desktop/fraud-detection-project
.venv/Scripts/python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Start the Frontend

```bash
cd /c/Users/LENOVO/Desktop/fraud-detection-project/frontend
python -m http.server 3000
```

### Access the Application

Open your browser and navigate to: `http://localhost:3000`

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000`:

- **Pre-approval endpoint**: `POST /predict`
- **Post-processing endpoint**: `POST /predict/post-processing`
- **Health check**: `GET /health`

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # Modern CSS with animations
├── app.js          # JavaScript for API integration
└── README.md       # This file
```

## Features Breakdown

### Transaction Form
- Transaction type selection (CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER)
- Step, amount, and balance fields
- Optional post-processing fields for enhanced analysis
- Real-time validation

### Results Panel
- Status indicator (legitimate/fraud)
- Fraud probability with visual bar
- Model information
- Features analyzed list
- Warning disclaimer

### Model Information
- Pre-approval model: 99.9% accuracy
- Post-processing model: 99.99% accuracy
- Response time: < 100ms

## Customization

### Colors
Edit CSS variables in `styles.css`:

```css
:root {
    --primary: #6366f1;
    --secondary: #10b981;
    --danger: #ef4444;
    /* ... */
}
```

### API URL
Edit `API_BASE_URL` in `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Future Enhancements

- [ ] Add authentication
- [ ] Transaction history
- [ ] Advanced analytics dashboard
- [ ] Export results to CSV/PDF
- [ ] Real-time monitoring stream
- [ ] Multi-language support
