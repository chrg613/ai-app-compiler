import logging

logger = logging.getLogger(__name__)


class JSGenerator:
    """
    Generates production-ready JavaScript for generated applications.
    Provides common utilities and event handlers.
    """

    @staticmethod
    def generate() -> str:
        """Generate main app JavaScript file"""
        js = """// Generated Application JavaScript
// This file is auto-generated. Modify with caution.

console.log('[App] Application initialized');

// API Base URL
const API_BASE = '/api';

// Error handler
function handleError(error) {
    console.error('[Error]', error);
    alert('An error occurred: ' + (error.message || 'Unknown error'));
}

// API Helper: GET request
async function apiGet(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        handleError(error);
        return null;
    }
}

// API Helper: POST request
async function apiPost(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        handleError(error);
        return null;
    }
}

// API Helper: PUT request
async function apiPut(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        handleError(error);
        return null;
    }
}

// API Helper: DELETE request
async function apiDelete(endpoint) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        handleError(error);
        return null;
    }
}

// Generic Delete Handler
async function deleteRecord(entity, id) {
    if (!confirm(`Are you sure you want to delete this ${entity}?`)) {
        return;
    }
    
    const result = await apiDelete(`/${entity}/${id}`);
    if (result) {
        // Refresh the table if function exists
        const loadFunction = window[`load${entity}`];
        if (typeof loadFunction === 'function') {
            loadFunction();
        }
    }
}

// Format date helper
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format time helper
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle helper
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Local storage helpers
const storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => JSON.parse(localStorage.getItem(key)),
    remove: (key) => localStorage.removeItem(key),
    clear: () => localStorage.clear()
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('[App] DOM Ready');
    });
} else {
    console.log('[App] DOM Already Ready');
}

// Prevent form submission issues
document.addEventListener('submit', function(e) {
    if (e.target.hasAttribute('data-prevent-default')) {
        e.preventDefault();
    }
});

console.log('[App] All utilities loaded');
"""
        logger.info("[JSGen] Generated main JavaScript file")
        return js
