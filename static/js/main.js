const API_BASE = '/api';

// Check authentication status
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE}/auth/check`, {
            credentials: 'include'
        });
        const data = await response.json();
        return data.authenticated ? data.user : null;
    } catch (error) {
        console.error('Auth check failed:', error);
        return null;
    }
}

// Update navigation based on auth status
async function updateNav() {
    const user = await checkAuth();
    const authLinks = document.getElementById('auth-links');
    
    if (!authLinks) return;
    
    if (user) {
        authLinks.innerHTML = `
            <div class="user-info">
                <div class="user-avatar">${user.username.charAt(0).toUpperCase()}</div>
                <span>${user.username}</span>
                <a href="/dashboard" class="btn btn-primary">Dashboard</a>
                <button onclick="logout()" class="btn btn-secondary">Logout</button>
            </div>
        `;
    } else {
        authLinks.innerHTML = `
            <a href="/login">Login</a>
            <a href="/signup" class="btn btn-primary">Sign Up</a>
        `;
    }
}

// Logout function
async function logout() {
    try {
        await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = '/';
    } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed. Please try again.');
    }
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Copy to clipboard
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = originalText;
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Failed to copy to clipboard');
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateNav();
});
