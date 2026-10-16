// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const form = document.getElementById('transactionForm');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsPlaceholder = document.getElementById('resultsPlaceholder');
const resultsContent = document.getElementById('resultsContent');
const resultStatus = document.getElementById('resultStatus');
const resultTitle = document.getElementById('resultTitle');
const resultSubtitle = document.getElementById('resultSubtitle');
const fraudProbability = document.getElementById('fraudProbability');
const fraudBar = document.getElementById('fraudBar');
const modelUsed = document.getElementById('modelUsed');
const featuresCount = document.getElementById('featuresCount');
const featuresList = document.getElementById('featuresList');

// Form Elements
const typeInput = document.getElementById('type');
const stepInput = document.getElementById('step');
const amountInput = document.getElementById('amount');
const oldbalanceorgInput = document.getElementById('oldbalanceorg');
const oldbalancedestInput = document.getElementById('oldbalancedest');
const newbalanceorigInput = document.getElementById('newbalanceorig');
const newbalancedestInput = document.getElementById('newbalancedest');

// Event Listeners
analyzeBtn.addEventListener('click', handleAnalyze);
clearBtn.addEventListener('click', handleClear);

// Handle Form Submission
async function handleAnalyze() {
    // Validate form
    if (!validateForm()) {
        return;
    }

    // Get form data
    const formData = {
        Step: parseInt(stepInput.value),
        Type: typeInput.value,
        Amount: parseFloat(amountInput.value),
        Oldbalanceorg: parseFloat(oldbalanceorgInput.value),
        Oldbalancedest: parseFloat(oldbalancedestInput.value),
    };

    // Add optional fields if provided
    if (newbalanceorigInput.value !== '') {
        formData.Newbalanceorig = parseFloat(newbalanceorigInput.value);
    }
    if (newbalancedestInput.value !== '') {
        formData.Newbalancedest = parseFloat(newbalancedestInput.value);
    }

    // Show loading state
    analyzeBtn.classList.add('loading');
    analyzeBtn.disabled = true;

    try {
        // Determine which endpoint to use
        const hasNewBalances = formData.Newbalanceorig !== undefined && formData.Newbalancedest !== undefined;
        const endpoint = hasNewBalances ? '/predict/post-processing' : '/predict';

        // Make API call
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        console.error('API URL:', API_BASE_URL);
        alert(`Error analyzing transaction: ${error.message}. Backend URL: ${API_BASE_URL}`);
    } finally {
        // Remove loading state
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = false;
    }
}

// Validate Form
function validateForm() {
    if (!typeInput.value) {
        alert('Please select a transaction type');
        typeInput.focus();
        return false;
    }
    if (!stepInput.value || stepInput.value < 0) {
        alert('Please enter a valid step value');
        stepInput.focus();
        return false;
    }
    if (!amountInput.value || amountInput.value < 0) {
        alert('Please enter a valid amount');
        amountInput.focus();
        return false;
    }
    if (!oldbalanceorgInput.value || oldbalanceorgInput.value < 0) {
        alert('Please enter a valid sender old balance');
        oldbalanceorgInput.focus();
        return false;
    }
    if (!oldbalancedestInput.value || oldbalancedestInput.value < 0) {
        alert('Please enter a valid receiver old balance');
        oldbalancedestInput.focus();
        return false;
    }
    return true;
}

// Display Results
function displayResults(data) {
    // Hide placeholder, show results
    resultsPlaceholder.classList.add('hidden');
    resultsContent.classList.remove('hidden');

    // Update status
    resultStatus.classList.remove('fraud', 'legitimate');
    if (data.prediction === 1) {
        resultStatus.classList.add('fraud');
        resultTitle.textContent = 'Potential Fraud Detected';
        resultSubtitle.textContent = 'Transaction shows suspicious patterns';
    } else {
        resultStatus.classList.add('legitimate');
        resultTitle.textContent = 'Legitimate Transaction';
        resultSubtitle.textContent = 'Transaction appears safe';
    }

    // Update fraud probability
    const probability = data.fraud_probability !== null ? (data.fraud_probability * 100).toFixed(1) : '0';
    fraudProbability.textContent = `${probability}%`;
    fraudBar.style.width = `${probability}%`;

    // Update fraud bar color based on probability
    if (probability > 50) {
        fraudBar.style.background = 'linear-gradient(135deg, #ef4444 0%, #f97316 100%)';
    } else if (probability > 20) {
        fraudBar.style.background = 'linear-gradient(135deg, #f59e0b 0%, #eab308 100%)';
    } else {
        fraudBar.style.background = 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)';
    }

    // Update model info
    modelUsed.textContent = data.model;
    featuresCount.textContent = data.features_used.length;

    // Update features list
    featuresList.innerHTML = '';
    data.features_used.forEach(feature => {
        const tag = document.createElement('span');
        tag.className = 'feature-tag';
        tag.textContent = feature;
        featuresList.appendChild(tag);
    });

    // Scroll to results on mobile
    if (window.innerWidth < 1024) {
        resultsContent.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Clear Form
function handleClear() {
    form.reset();
    resultsPlaceholder.classList.remove('hidden');
    resultsContent.classList.add('hidden');
}

// Visualization Tabs
const vizTabs = document.querySelectorAll('.viz-tab');
const vizPanels = document.querySelectorAll('.viz-panel');

vizTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove active class from all tabs and panels
        vizTabs.forEach(t => t.classList.remove('active'));
        vizPanels.forEach(p => p.classList.remove('active'));

        // Add active class to clicked tab and corresponding panel
        tab.classList.add('active');
        const tabId = tab.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
    });
});

// Check backend health on load
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('Backend health:', data);
            if (!data.preapproval_model_loaded || !data.postprocessing_model_loaded) {
                console.warn('One or more models are not loaded');
            }
        }
    } catch (error) {
        console.error('Backend not available:', error);
    }
}

// Initialize
checkBackendHealth();
