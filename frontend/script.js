/**
 * AI-Powered Hospital Scheduler - Frontend JavaScript
 * Handles API communication and UI interactions
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const predictionForm = document.getElementById('predictionForm');
const resultCard = document.getElementById('resultCard');
const waitTimeValue = document.getElementById('waitTimeValue');
const resultDetails = document.getElementById('resultDetails');
const apiStatus = document.getElementById('apiStatus');
const modelInfo = document.getElementById('modelInfo');
const predictBtn = document.getElementById('predictBtn');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    checkAPIHealth();
    loadModelInfo();
    setupFormHandlers();
    setDefaultValues();
});

/**
 * Check API health status
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy' && data.model_loaded) {
            updateAPIStatus('online', 'API Online');
        } else {
            updateAPIStatus('offline', 'Model Not Loaded');
        }
    } catch (error) {
        updateAPIStatus('offline', 'API Offline');
        console.error('API health check failed:', error);
    }
}

/**
 * Update API status badge
 */
function updateAPIStatus(status, text) {
    apiStatus.className = `status-badge ${status}`;
    apiStatus.querySelector('span:last-child').textContent = text;
}

/**
 * Load model information
 */
async function loadModelInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/model/info`);
        const data = await response.json();

        displayModelInfo(data);
    } catch (error) {
        console.error('Failed to load model info:', error);
        modelInfo.innerHTML = `
            <div class="info-item">
                <div class="info-label">Status</div>
                <div class="info-value">Unable to load model information</div>
            </div>
        `;
    }
}

/**
 * Display model information
 */
function displayModelInfo(data) {
    const metrics = data.metrics.wait_time || {};

    modelInfo.innerHTML = `
        <div class="info-item">
            <div class="info-label">Model Type</div>
            <div class="info-value">${data.model_type}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Test R² Score</div>
            <div class="info-value">${(metrics.test_r2 || 0).toFixed(4)}</div>
        </div>
        <div class="info-item">
            <div class="info-label">Test RMSE</div>
            <div class="info-value">${(metrics.test_rmse || 0).toFixed(2)} min</div>
        </div>
        <div class="info-item">
            <div class="info-label">Test MAE</div>
            <div class="info-value">${(metrics.test_mae || 0).toFixed(2)} min</div>
        </div>
        <div class="info-item">
            <div class="info-label">Features</div>
            <div class="info-value">${data.features.length} features</div>
        </div>
    `;
}

/**
 * Setup form event handlers
 */
function setupFormHandlers() {
    predictionForm.addEventListener('submit', handlePrediction);

    // Auto-set weekend based on day selection
    const daySelect = document.getElementById('day_of_week');
    const weekendSelect = document.getElementById('is_weekend');

    daySelect.addEventListener('change', (e) => {
        const day = e.target.value;
        weekendSelect.value = (day === 'Saturday' || day === 'Sunday') ? '1' : '0';
    });
}

/**
 * Set default form values for quick testing
 */
function setDefaultValues() {
    const now = new Date();
    document.getElementById('arrival_hour').value = now.getHours();
    document.getElementById('patient_age').value = 45;
    document.getElementById('num_available_doctors').value = 5;
    document.getElementById('num_available_nurses').value = 8;
    document.getElementById('num_available_rooms').value = 10;
    document.getElementById('current_queue_length').value = 15;
}

/**
 * Handle prediction form submission
 */
async function handlePrediction(e) {
    e.preventDefault();

    // Show loading state
    setLoadingState(true);

    // Collect form data
    const formData = new FormData(predictionForm);
    const patientData = {};

    for (let [key, value] of formData.entries()) {
        // Convert numeric fields
        if (['arrival_hour', 'patient_age', 'num_available_doctors',
            'num_available_nurses', 'num_available_rooms',
            'current_queue_length', 'is_weekend'].includes(key)) {
            patientData[key] = parseInt(value);
        } else {
            patientData[key] = value;
        }
    }

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patientData)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const result = await response.json();
        displayPrediction(result);

    } catch (error) {
        console.error('Prediction failed:', error);
        showError('Failed to get prediction. Please ensure the API is running.');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Display prediction results
 */
function displayPrediction(result) {
    const waitTime = result.predicted_wait_time_minutes;
    const input = result.input_data;

    // Update wait time display
    waitTimeValue.textContent = Math.round(waitTime);

    // Create result details
    resultDetails.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Department</div>
            <div class="detail-value">${input.department}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Priority</div>
            <div class="detail-value">${input.priority}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Patient Age</div>
            <div class="detail-value">${input.patient_age} years</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Queue Length</div>
            <div class="detail-value">${input.current_queue_length} patients</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Available Doctors</div>
            <div class="detail-value">${input.num_available_doctors}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Available Nurses</div>
            <div class="detail-value">${input.num_available_nurses}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Available Rooms</div>
            <div class="detail-value">${input.num_available_rooms}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Time</div>
            <div class="detail-value">${input.arrival_hour}:00, ${input.day_of_week}</div>
        </div>
    `;

    // Show result card with animation
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Show error message
 */
function showError(message) {
    resultDetails.innerHTML = `
        <div class="detail-item" style="grid-column: 1 / -1; background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3);">
            <div class="detail-label">Error</div>
            <div class="detail-value" style="color: #ef4444;">${message}</div>
        </div>
    `;

    waitTimeValue.textContent = '--';
    resultCard.style.display = 'block';
}

/**
 * Set loading state
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        predictBtn.disabled = true;
        predictBtn.innerHTML = `
            <span>Predicting...</span>
            <div class="loading"></div>
        `;
    } else {
        predictBtn.disabled = false;
        predictBtn.innerHTML = `
            <span>Predict Wait Time</span>
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
        `;
    }
}

/**
 * Periodically check API health
 */
setInterval(checkAPIHealth, 30000); // Check every 30 seconds
