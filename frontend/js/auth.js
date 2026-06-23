/* Telegram Mini App Authentication Module

   Manages the entire authentication lifecycle: initialising the Telegram
   Mini App session, registering new RPG characters, and logging out.

   Flow (startup):
   1. window.addEventListener('load', initializeTelegramSession) — fires as
      soon as the page finishes loading.
   2. getTelegramWebApp() retrieves the window.Telegram.WebApp object that
      Telegram injects into the Mini App iframe.
   3. If the WebApp object or its initData is missing, the user is shown a
      message instructing them to open the app from Telegram.
   4. Otherwise, tg.ready() and tg.expand() tell Telegram the app is ready,
      and the raw initData is stored in authManager.initData.
   5. api.telegramSession() sends the initData to the backend, which
      cryptographically verifies the payload and looks up the user.
   6. If the user already has a character → switchToGameScreen().
      If not → show the registration form with Telegram data pre-filled.

   Dependencies:
   - api (APIClient from api.js) — all backend communication.
   - switchToRegister, switchToGameScreen, switchToAuthScreen (ui.js) —
     screen transitions.
   - authManager (AuthManager, this file) — in-memory state holder for the
     current authenticated user.
*/

// =========================================================================
// AuthManager — light-weight state container
// =========================================================================

class AuthManager {
    /**
     * Holds the current authenticated user object and the raw Telegram
     * initData. Both are cleared on logout.
     *
     * Why not localStorage?
     * Telegram Mini App sessions are ephemeral — the Telegram client manages
     * re-authorisation. Storing tokens in the browser would only add
     * complexity without benefit.
     */
    constructor() {
        this.currentUser = null;
        this.telegramUser = null;
        this.initData = '';
    }

    /** Persist the authenticated user (called after login or register). */
    setCurrentUser(user) {
        this.currentUser = user;
    }

    /** Remove the authenticated user (called on logout). */
    clearCurrentUser() {
        this.currentUser = null;
    }

    /** Quick check — the UI uses this to decide which screen to show. */
    isLoggedIn() {
        return this.currentUser !== null;
    }

    /** Retrieve the current user object for display. */
    getCurrentUser() {
        return this.currentUser;
    }
}

// Global singleton — the one source of truth for the current session.
const authManager = new AuthManager();
let tg = null;

// =========================================================================
// UI helpers — update the welcome / error messages on the auth screen
// =========================================================================

/**
 * Update the welcome message text (e.g. "Opening the guild gates...").
 * These are small status hints shown on the login-form screen.
 */
function setAuthMessage(message) {
    const messageElement = document.getElementById('welcome-message');
    if (messageElement) {
        messageElement.textContent = message;
    }
}

/**
 * Show a red error banner on the login-form screen.
 * Hidden by default (class "error-message" → display: none);
 * adding "show" switches it to display: block.
 * The caller provides the message; this function only reveals it.
 */
function showAuthError(message) {
    const errorDiv = document.getElementById('login-error');
    if (!errorDiv) return;

    errorDiv.textContent = message;
    errorDiv.classList.add('show');
}

// =========================================================================
// Telegram WebApp helpers
// =========================================================================

/**
 * Safely retrieve the Telegram.WebApp object injected by the Telegram
 * client into the Mini App iframe. Returns null when the app is opened
 * outside of Telegram (e.g. in a regular browser for testing).
 *
 * The global 'tg' variable is set once by initializeTelegramSession()
 * and used by later calls to tg.ready() / tg.expand().
 */
function getTelegramWebApp() {
    if (window.Telegram && window.Telegram.WebApp) {
        return window.Telegram.WebApp;
    }

    return null;
}

/**
 * Pre-fill the registration form fields with data from the Telegram user
 * profile (username, first name) to reduce typing friction. Called after
 * a successful initData verification when no existing character is found.
 */
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

// =========================================================================
// Core authentication flow
// =========================================================================

/**
 * Main entry point — called once on page load via the load event listener
 * at the bottom of this file. Obtains the Telegram.WebApp object and its
 * initData, then resolves the session on the backend.
 *
 * Steps:
 * 1. Retrieve the Telegram.WebApp object.
 * 2. If it is unavailable → show an offline hint and stop.
 * 3. Signal readiness to Telegram (tg.ready()) and expand to full height.
 * 4. Store the raw initData in authManager.initData.
 * 5. Send the initData to the backend for cryptographic verification.
 * 6. Based on the server response:
 *    - Already registered → jump to the game screen.
 *    - Not registered → show the registration form with Telegram data.
 * 7. On any error → display a user-friendly message on the auth screen.
 */
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

        if (!response.telegram_user) {
            throw new Error('Server did not return Telegram user data');
        }

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

/**
 * Register a new RPG character via the Telegram flow.
 *
 * Triggered by clicking the "Enter the Realm" button on the registration
 * form. Performs client-side validation (username length and character
 * set) as a fast preliminary check — the backend (auth_routes.py) runs
 * its own identical validation and returns a detailed error if it fails.
 * On success, stores the user and transitions to the game screen after a
 * short delay.
 *
 * NOTE: The legacy methods api.register() and api.login() (username +
 * password) exist in api.js but are not called here. They are kept for
 * future use when a password-based registration form is added.
 */
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

    // Preliminary client-side validation (fast feedback; backend enforces
    // the same rules so this can safely be relaxed without breaking security)
    if (!username || username.length < 3) {
        errorDiv.textContent = 'Username must be at least 3 characters';
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

// =========================================================================
// Login / Logout
// =========================================================================

/**
 * Legacy login — retry session resolution without re-initialising the
 * Telegram WebApp object (tg.ready() and tg.expand() are called only once
 * during initializeTelegramSession). If initData has already been captured,
 * this function re-verifies it on the backend. Otherwise, it falls back to
 * a full initialisation flow.
 *
 * Kept as a separate entry point so the HTML can target a distinct button
 * in case the password-based flow diverges in the future.
 */
async function loginUser() {
    if (!authManager.initData) {
        // No initData captured yet — delegate to the full bootstrap.
        return initializeTelegramSession();
    }

    setAuthMessage('Checking your adventurer seal...');

    try {
        const response = await api.telegramSession(authManager.initData);

        if (!response.telegram_user) {
            throw new Error('Server did not return Telegram user data');
        }

        authManager.telegramUser = response.telegram_user;

        if (response.registered && response.user) {
            authManager.setCurrentUser(response.user);
            switchToGameScreen();
        } else {
            setAuthMessage('Welcome, traveler. Create your character to begin.');
            prefillCharacterForm(response.telegram_user);
            document.getElementById('create-character-button').hidden = false;
            switchToRegister();
        }
    } catch (error) {
        setAuthMessage('The guild could not verify your Telegram session.');
        showAuthError(error.message);
    }
}

/**
 * Log out the current user and return to the auth screen.
 * Clears authManager state and shows a message explaining that the user
 * must re-open the Mini App from Telegram to authenticate again.
 */
function logout() {
    authManager.clearCurrentUser();
    switchToAuthScreen();
    setAuthMessage('Telegram keeps your identity sealed. Reopen the app to enter again.');
}

// =========================================================================
// Bootstrap — start the session as soon as the DOM is ready
// =========================================================================

window.addEventListener('load', initializeTelegramSession);
