/**
 * MailSpectre Frontend JavaScript
 * Handles email validation requests and UI updates
 */

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000',
    API_ENDPOINT: '/api/validate',
    REQUEST_TIMEOUT: 10000
};

// DOM Elements
const elements = {
    emailInput: document.getElementById('emailInput'),
    validateBtn: document.getElementById('validateBtn'),
    btnText: document.querySelector('.btn-text'),
    btnLoader: document.querySelector('.btn-loader'),
    resultsSection: document.getElementById('resultsSection'),
    errorSection: document.getElementById('errorSection'),
    overallStatus: document.getElementById('overallStatus'),
    emailDisplay: document.getElementById('emailDisplay'),
    scoreBar: document.getElementById('scoreBar'),
    scoreText: document.getElementById('scoreText'),
    summaryText: document.getElementById('summaryText'),
    checksGrid: document.getElementById('checksGrid'),
    jsonOutput: document.getElementById('jsonOutput'),
    copyJsonBtn: document.getElementById('copyJsonBtn'),
    errorMessage: document.getElementById('errorMessage')
};

// State
let currentResult = null;

/**
 * Initialize event listeners
 */
function init() {
    // Validate button click
    elements.validateBtn.addEventListener('click', handleValidation);
    
    // Enter key in input
    elements.emailInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleValidation();
        }
    });
    
    // Copy JSON button
    elements.copyJsonBtn.addEventListener('click', copyJsonToClipboard);
    
    // Clear input on focus if empty
    elements.emailInput.addEventListener('focus', () => {
        hideError();
    });
    
    console.log('MailSpectre initialized');
}

/**
 * Handle email validation
 */
async function handleValidation() {
    const email = elements.emailInput.value.trim();
    
    // Basic validation
    if (!email) {
        showError('Please enter an email address');
        return;
    }
    
    // Hide previous results
    hideResults();
    hideError();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Make API request
        const result = await validateEmail(email);
        
        // Store result
        currentResult = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Validation error:', error);
        showError(error.message || 'An error occurred during validation');
    } finally {
        setLoadingState(false);
    }
}

/**
 * Call API to validate email
 * @param {string} email - Email address to validate
 * @returns {Promise<Object>} Validation result
 */
async function validateEmail(email) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), CONFIG.REQUEST_TIMEOUT);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email }),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.message || data.error || 'Validation failed');
        }
        
        return data;
        
    } catch (error) {
        clearTimeout(timeoutId);
        
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please try again.');
        }
        
        if (error.message.includes('fetch')) {
            throw new Error('Cannot connect to validation server. Make sure the backend is running.');
        }
        
        throw error;
    }
}

/**
 * Display validation results
 * @param {Object} result - Validation result object
 */
function displayResults(result) {
    // Show results section
    elements.resultsSection.style.display = 'block';
    
    // Overall status
    elements.overallStatus.textContent = result.valid ? '✓ Valid' : '✗ Invalid';
    elements.overallStatus.className = `status-badge ${result.valid ? 'valid' : 'invalid'}`;
    
    // Email display
    elements.emailDisplay.textContent = result.email;
    
    // Score
    displayScore(result.score);
    
    // Summary
    elements.summaryText.textContent = result.summary;
    
    // Checks
    displayChecks(result.checks);
    
    // JSON output
    elements.jsonOutput.textContent = JSON.stringify(result, null, 2);
    
    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Display validation score
 * @param {number} score - Score percentage
 */
function displayScore(score) {
    const scoreClass = score >= 80 ? 'high' : score >= 60 ? 'medium' : 'low';
    
    elements.scoreBar.style.width = `${score}%`;
    elements.scoreBar.className = `score-fill ${scoreClass}`;
    elements.scoreText.textContent = `${score}%`;
}

/**
 * Display individual checks
 * @param {Array} checks - Array of check objects
 */
function displayChecks(checks) {
    // Clear existing checks
    elements.checksGrid.innerHTML = '';
    
    // Create check cards
    checks.forEach(check => {
        const checkCard = createCheckCard(check);
        elements.checksGrid.appendChild(checkCard);
    });
}

/**
 * Create a check card element
 * @param {Object} check - Check object
 * @returns {HTMLElement} Check card element
 */
function createCheckCard(check) {
    const card = document.createElement('div');
    card.className = 'check-card';
    
    // Format check name
    const checkName = check.check.replace(/_/g, ' ');
    
    // Determine icon
    const icon = check.valid ? '✓' : '✗';
    const statusClass = check.valid ? 'valid' : 'invalid';
    
    card.innerHTML = `
        <div class="check-header">
            <div class="check-name">${checkName}</div>
            <div class="check-icon ${statusClass}">${icon}</div>
        </div>
        <div class="check-message ${statusClass}">${check.message}</div>
        <div class="check-details">${check.details}</div>
    `;
    
    return card;
}

/**
 * Copy JSON output to clipboard
 */
async function copyJsonToClipboard() {
    try {
        const jsonText = elements.jsonOutput.textContent;
        await navigator.clipboard.writeText(jsonText);
        
        // Visual feedback
        const originalText = elements.copyJsonBtn.querySelector('.copy-text').textContent;
        elements.copyJsonBtn.classList.add('copied');
        elements.copyJsonBtn.querySelector('.copy-text').textContent = 'Copied!';
        
        setTimeout(() => {
            elements.copyJsonBtn.classList.remove('copied');
            elements.copyJsonBtn.querySelector('.copy-text').textContent = originalText;
        }, 2000);
        
    } catch (error) {
        console.error('Failed to copy:', error);
        alert('Failed to copy to clipboard');
    }
}

/**
 * Show error message
 * @param {string} message - Error message
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorSection.style.display = 'block';
    elements.errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/**
 * Hide error message
 */
function hideError() {
    elements.errorSection.style.display = 'none';
}

/**
 * Hide results section
 */
function hideResults() {
    elements.resultsSection.style.display = 'none';
}

/**
 * Set loading state
 * @param {boolean} isLoading - Loading state
 */
function setLoadingState(isLoading) {
    elements.validateBtn.disabled = isLoading;
    elements.emailInput.disabled = isLoading;
    
    if (isLoading) {
        elements.btnText.style.display = 'none';
        elements.btnLoader.style.display = 'inline-block';
    } else {
        elements.btnText.style.display = 'inline';
        elements.btnLoader.style.display = 'none';
    }
}

/**
 * Check if backend is running
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/health`, {
            method: 'GET',
            signal: AbortSignal.timeout(3000)
        });
        
        if (response.ok) {
            console.log('✓ Backend is running');
            return true;
        }
    } catch (error) {
        console.warn('⚠ Backend is not responding. Make sure to start the Flask server.');
        return false;
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    init();
    checkBackendHealth();
});

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateEmail,
        displayResults,
        createCheckCard
    };
}
