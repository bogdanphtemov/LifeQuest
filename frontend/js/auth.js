/* Telegram Mini App Authentication Module */

class AuthManager {
    constructor() {
        this.currentUser = null;
        this.telegramUser = null;
        this.initData = '';
    }

    setCurrentUser(user) {
        this.currentUser = user;
    }

    clearCurrentUser() {
        this.currentUser = null;
    }

    isLoggedIn() {
        return this.currentUser !== null;
    }

    getCurrentUser() {
        return this.currentUser;
    }
}

const authManager = new AuthManager();
let tg = null;

function setAuthMessage(message) {
    const messageElement = document.getElementById('welcome-message');
    if (messageElement) {
        messageElement.textContent = message;
    }
}

function showAuthError(message) {
    const errorDiv = document.getElementById('login-error');
    if (!errorDiv) return;

    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

function getTelegramWebApp() {
    if (window.Telegram && window.Telegram.WebApp) {
        return window.Telegram.WebApp;
    }

    return null;
}

function prefillCharacterForm(telegramUser) {
    const usernameInput = document.getElementById('reg-username');
    const displayNameInput = document.getElementById('reg-display-name');

    if (usernameInput && telegramUser?.username) {
        usernameInput.value = telegramUser.username;
    }

    if (displayNameInput) {
        displayNameInput.value = telegramUser?.first_name || telegramUser?.username || '';
    }
}

async function initializeTelegramSession() {
    tg = getTelegramWebApp();

    if (!tg || !tg.initData) {
        setAuthMessage('Open this app from Telegram to enter the realm.');
        showAuthError('Telegram authorization data was not found.');
        return;
    }

    tg.ready();
    tg.expand();
    authManager.initData = tg.initData;
    setAuthMessage('Checking your adventurer seal...');

    try {
        const response = await api.telegramSession(authManager.initData);
        authManager.telegramUser = response.telegram_user;

        if (response.registered && response.user) {
            authManager.setCurrentUser(response.user);
            switchToGameScreen();
            return;
        }

        setAuthMessage('Welcome, traveler. Create your character to begin.');
        prefillCharacterForm(response.telegram_user);
        document.getElementById('create-character-button').hidden = false;
        switchToRegister();
    } catch (error) {
        setAuthMessage('The guild could not verify your Telegram session.');
        showAuthError(error.message);
    }
}

async function registerUser() {
    const username = document.getElementById('reg-username').value.trim();
    const displayName = document.getElementById('reg-display-name').value.trim();
    const characterClass = document.getElementById('reg-class').value;
    const errorDiv = document.getElementById('register-error');
    const successDiv = document.getElementById('register-success');

    errorDiv.classList.remove('show');
    successDiv.classList.remove('show');

    if (!authManager.initData) {
        errorDiv.textContent = 'Open this app from Telegram to create a character.';
        errorDiv.classList.add('show');
        return;
    }

    if (!username || username.length < 3 || username.length > 20) {
        errorDiv.textContent = 'Username must be 3-20 characters';
        errorDiv.classList.add('show');
        return;
    }

    if (!username.replaceAll('_', '').replaceAll('-', '').match(/^[a-zA-Z0-9]+$/)) {
        errorDiv.textContent = 'Username can only contain letters, numbers, hyphens, and underscores';
        errorDiv.classList.add('show');
        return;
    }

    try {
        const response = await api.telegramRegister(
            authManager.initData,
            username,
            displayName,
            characterClass,
        );

        authManager.setCurrentUser(response.user);
        successDiv.textContent = 'Registration successful. Entering the realm...';
        successDiv.classList.add('show');

        setTimeout(() => {
            switchToGameScreen();
        }, 800);
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
}

function loginUser() {
    initializeTelegramSession();
}

function logout() {
    authManager.clearCurrentUser();
    switchToAuthScreen();
    setAuthMessage('Telegram keeps your identity sealed. Reopen the app to enter again.');
}

window.addEventListener('load', initializeTelegramSession);
