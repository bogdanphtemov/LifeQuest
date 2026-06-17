/* Authentication Module */

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.loadUserFromStorage();
    }

    saveUserToStorage(user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUser = user;
    }

    loadUserFromStorage() {
        const stored = localStorage.getItem('currentUser');
        if (stored) {
            this.currentUser = JSON.parse(stored);
        }
    }

    clearUserStorage() {
        localStorage.removeItem('currentUser');
        this.currentUser = null;
    }

    isLoggedIn() {
        return this.currentUser !== null;
    }

    getCurrentUser() {
        return this.currentUser;
    }
}

// Global auth manager
const authManager = new AuthManager();

// Telegram Web App integration (optional)
let tg = null;
let telegramUserId = null;

if (typeof window.Telegram !== 'undefined' && window.Telegram.WebApp) {
    tg = window.Telegram.WebApp;
    tg.expand();
    const user = tg.initDataUnsafe?.user;
    if (user) {
        telegramUserId = user.id;
    }
}

// Fallback: use mock telegram ID for testing
if (!telegramUserId) {
    telegramUserId = 123456789; // For testing
}

async function registerUser() {
    const username = document.getElementById('reg-username').value.trim();
    const password = document.getElementById('reg-password').value;
    const firstName = document.getElementById('reg-first-name').value.trim();
    const lastName = document.getElementById('reg-last-name').value.trim();
    const errorDiv = document.getElementById('register-error');
    const successDiv = document.getElementById('register-success');

    // Clear messages
    errorDiv.classList.remove('show');
    successDiv.classList.remove('show');

    // Validate
    if (!username || username.length < 3 || username.length > 20) {
        errorDiv.textContent = 'Username must be 3-20 characters';
        errorDiv.classList.add('show');
        return;
    }

    if (!password || password.length < 6) {
        errorDiv.textContent = 'Password must be at least 6 characters';
        errorDiv.classList.add('show');
        return;
    }

    try {
        const response = await api.register(username, password, telegramUserId, firstName, lastName);
        
        authManager.saveUserToStorage(response.user);
        successDiv.textContent = '✅ Registration successful! Redirecting...';
        successDiv.classList.add('show');

        setTimeout(() => {
            switchToGameScreen();
        }, 2000);
    } catch (error) {
        errorDiv.textContent = `❌ ${error.message}`;
        errorDiv.classList.add('show');
    }
}

async function loginUser() {
    const username = document.getElementById('login-username').value.trim();
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    errorDiv.classList.remove('show');

    if (!username) {
        errorDiv.textContent = 'Please enter your username';
        errorDiv.classList.add('show');
        return;
    }

    if (!password) {
        errorDiv.textContent = 'Please enter your password';
        errorDiv.classList.add('show');
        return;
    }

    try {
        const response = await api.login(username, password, telegramUserId);
        
        authManager.saveUserToStorage(response.user);
        switchToGameScreen();
    } catch (error) {
        errorDiv.textContent = `❌ ${error.message}`;
        errorDiv.classList.add('show');
    }
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        authManager.clearUserStorage();
        switchToAuthScreen();
    }
}

// Check if already logged in on page load
window.addEventListener('load', () => {
    if (authManager.isLoggedIn()) {
        switchToGameScreen();
    }
});
