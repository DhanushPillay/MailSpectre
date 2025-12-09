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
        // Check if backend is running first
        const isBackendRunning = await checkBackendHealth();
        
        if (!isBackendRunning) {
            // Show helpful error message with instructions
            showError(`🚨 Backend server is not running!
            
📝 To start the backend:
1. Open a terminal
2. Navigate to: E:\\Personal Projects\\MailSpectre\\backend
3. Run: python app.py

The server should start on http://localhost:5000`);
            return;
        }
        
        // Make API request
        const result = await validateEmail(email);
        
        // Store result
        currentResult = result;
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Validation error:', error);
        
        // Better error message for connection issues
        if (error.message.includes('connect') || error.message.includes('fetch')) {
            showError(`❌ Cannot connect to backend server.
            
Please start the backend by running:
cd "E:\\Personal Projects\\MailSpectre\\backend"
python app.py`);
        } else {
            showError(error.message || 'An error occurred during validation');
        }
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
    
    // Special handling for email_type check - always show as informational
    if (check.check === 'email_type') {
        card.className = 'group relative flex flex-col overflow-hidden rounded-xl border border-accent-cyan/30 bg-accent-cyan/10 p-5 transition-all duration-300 hover:border-accent-cyan/60 hover:bg-accent-cyan/20';
        
        // Email type badges with emojis
        const typeBadges = {
            'student': { emoji: '🎓', label: 'Student', color: 'bg-purple-500/20 text-purple-300', border: 'border-purple-500/40' },
            'work': { emoji: '💼', label: 'Work', color: 'bg-blue-500/20 text-blue-300', border: 'border-blue-500/40' },
            'personal': { emoji: '👤', label: 'Personal', color: 'bg-green-500/20 text-green-300', border: 'border-green-500/40' },
            'temporary': { emoji: '⏱️', label: 'Temporary', color: 'bg-orange-500/20 text-orange-300', border: 'border-orange-500/40' },
            'unknown': { emoji: '❓', label: 'Unknown', color: 'bg-gray-500/20 text-gray-300', border: 'border-gray-500/40' }
        };
        
        const typeInfo = typeBadges[check.email_type] || typeBadges['unknown'];
        const confidenceColor = check.confidence >= 90 ? 'text-accent-lime' : 
                               check.confidence >= 75 ? 'text-accent-cyan' : 
                               check.confidence >= 60 ? 'text-yellow-400' : 'text-orange-400';
        
        card.innerHTML = `
            <div class="flex items-start justify-between mb-2">
                <h3 class="font-medium text-white">Email Type</h3>
                <div class="flex h-7 w-7 items-center justify-center rounded-full bg-accent-cyan/20 text-accent-cyan">
                    <span class="material-symbols-outlined text-xl">info</span>
                </div>
            </div>
            <div class="flex items-center gap-2 mb-2">
                <span class="inline-flex items-center gap-1.5 rounded-lg border ${typeInfo.border} ${typeInfo.color} px-3 py-1.5 text-sm font-semibold">
                    <span>${typeInfo.emoji}</span>
                    <span>${typeInfo.label}</span>
                </span>
                <span class="text-xs ${confidenceColor} font-medium">${check.confidence}%</span>
            </div>
            <p class="text-xs text-white/70 mt-2">${check.details}</p>
            ${check.company ? `<p class="text-xs text-accent-cyan font-medium mt-1">🏢 ${check.company}</p>` : ''}
        `;
        
        return card;
    }
    
    // Special handling for typo suggestions
    if (check.check === 'typo_detection' && check.suggestion) {
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
                <div class="mt-2 rounded-lg bg-accent-cyan/10 border border-accent-cyan/30 px-3 py-2">
                    <p class="text-xs text-accent-cyan font-medium">💡 Did you mean: ${check.suggestion}</p>
                </div>
            </div>
        `;
        return card;
    }
    
    // Special handling for data breach warnings
    if (check.check === 'data_breach' && !check.valid && check.breach_count) {
        card.innerHTML = `
            <div class="flex items-start justify-between">
                <h3 class="font-medium text-white">${checkName}</h3>
                <div class="flex h-7 w-7 items-center justify-center rounded-full ${iconBg} ${iconColor}">
                    <span class="material-symbols-outlined text-xl">warning</span>
                </div>
            </div>
            <div class="mt-auto pt-3">
                <p class="text-sm font-medium ${textColor}">${check.message}</p>
                <p class="mt-1 text-xs text-white/60">${check.details}</p>
                <div class="mt-2 rounded-lg bg-accent-red/10 border border-accent-red/30 px-3 py-2">
                    <p class="text-xs text-accent-red font-bold">⚠️ Found in ${check.breach_count} data breach(es)</p>
                    <p class="text-xs text-white/60 mt-1">Recommend changing password immediately</p>
                </div>
            </div>
        `;
        return card;
    }
    
    // Special handling for suspicious TLD
    if (check.check === 'suspicious_tld' && !check.valid && check.tld) {
        card.innerHTML = `
            <div class="flex items-start justify-between">
                <h3 class="font-medium text-white">${checkName}</h3>
                <div class="flex h-7 w-7 items-center justify-center rounded-full ${iconBg} ${iconColor}">
                    <span class="material-symbols-outlined text-xl">warning</span>
                </div>
            </div>
            <div class="mt-auto pt-3">
                <p class="text-sm font-medium ${textColor}">${check.message}</p>
                <p class="mt-1 text-xs text-white/60">${check.details}</p>
                <div class="mt-2 rounded-lg bg-orange-500/10 border border-orange-500/30 px-3 py-2">
                    <p class="text-xs text-orange-400 font-medium">⚠️ Domain uses ${check.tld}</p>
                    <p class="text-xs text-white/60 mt-1">Often associated with spam/phishing</p>
                </div>
            </div>
        `;
        return card;
    }
    
    // Default card for other checks
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
            signal: AbortSignal.timeout(2000)
        });
        
        if (response.ok) {
            console.log('✓ Backend is running');
            updateBackendStatus(true);
            return true;
        }
        updateBackendStatus(false);
        return false;
    } catch (error) {
        console.warn('⚠ Backend is not responding.');
        updateBackendStatus(false);
        return false;
    }
}

/**
 * Update backend status indicator
 */
function updateBackendStatus(isRunning) {
    const statusIndicator = document.getElementById('backendStatus');
    if (statusIndicator) {
        if (isRunning) {
            statusIndicator.innerHTML = '🟢 Backend Online';
            statusIndicator.className = 'text-xs text-accent-lime';
        } else {
            statusIndicator.innerHTML = '🔴 Backend Offline';
            statusIndicator.className = 'text-xs text-accent-red';
        }
    }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    init();
    checkBackendHealth();
    
    // Check backend status every 10 seconds
    setInterval(checkBackendHealth, 10000);
});
