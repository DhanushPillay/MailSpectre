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
    resultsSection: document.getElementById('resultsSection'),
    errorSection: document.getElementById('errorSection'),
    overallStatus: document.getElementById('overallStatus'),
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
    elements.resultsSection.classList.remove('hidden');
    
    // Overall status
    if (result.valid) {
        elements.overallStatus.textContent = 'VALID';
        elements.overallStatus.className = 'mt-2 text-4xl font-bold text-accent-lime drop-shadow-[0_0_15px_rgba(57,255,20,0.7)]';
    } else {
        elements.overallStatus.textContent = 'INVALID';
        elements.overallStatus.className = 'mt-2 text-4xl font-bold text-accent-red drop-shadow-[0_0_15px_rgba(255,65,54,0.7)]';
    }
    
    // Checks
    displayChecks(result.checks);
    
    // JSON output
    elements.jsonOutput.textContent = JSON.stringify(result, null, 2);
    
    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
    
    // Format check name
    const checkName = check.check.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    
    // Determine styles based on validity
    const isValid = check.valid;
    const borderColor = isValid ? 'hover:border-accent-lime/80' : 'hover:border-accent-red/80';
    const bgColor = isValid ? 'hover:bg-accent-lime/10' : 'hover:bg-accent-red/10';
    const iconColor = isValid ? 'text-accent-lime' : 'text-accent-red';
    const iconBg = isValid ? 'bg-accent-lime/20' : 'bg-accent-red/20';
    const icon = isValid ? 'check' : 'close';
    const textColor = isValid ? 'text-accent-lime' : 'text-accent-red';
    
    card.className = `group relative flex flex-col overflow-hidden rounded-xl border border-white/10 bg-white/5 p-5 transition-all duration-300 ${borderColor} ${bgColor}`;
    
    card.innerHTML = `
        <div class="flex items-start justify-between">
            <h3 class="font-medium text-white">${checkName}</h3>
            <div class="flex h-7 w-7 items-center justify-center rounded-full ${iconBg} ${iconColor}">
                <span class="material-symbols-outlined text-xl">${icon}</span>
            </div>
        </div>
        <div class="mt-auto pt-3">
            <p class="text-sm font-medium ${textColor}">${check.message}</p>
            <p class="mt-1 text-xs text-white/60">${check.details}</p>
        </div>
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
        const btn = elements.copyJsonBtn;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.classList.add('bg-accent-lime/20', 'text-accent-lime');
        
        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('bg-accent-lime/20', 'text-accent-lime');
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
    elements.errorSection.classList.remove('hidden');
}

/**
 * Hide error message
 */
function hideError() {
    elements.errorSection.classList.add('hidden');
}

/**
 * Hide results section
 */
function hideResults() {
    elements.resultsSection.classList.add('hidden');
}

/**
 * Set loading state
 * @param {boolean} isLoading - Loading state
 */
function setLoadingState(isLoading) {
    elements.validateBtn.disabled = isLoading;
    elements.emailInput.disabled = isLoading;
    
    const btnSpan = elements.validateBtn.querySelector('span');
    if (isLoading) {
        btnSpan.textContent = 'Inspecting...';
        elements.validateBtn.classList.add('opacity-75', 'cursor-wait');
    } else {
        btnSpan.textContent = 'Inspect';
        elements.validateBtn.classList.remove('opacity-75', 'cursor-wait');
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
