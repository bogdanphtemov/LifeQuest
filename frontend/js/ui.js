/* UI Management Module

   This module handles screen transitions (auth ↔ game), form switching
   (login ↔ register), and player info updates. All DOM event listeners
   are registered here as an alternative to inline onclick handlers in the
   HTML — this improves CSP compliance, testability, and keeps concerns
   separated.
*/

// =========================================================================
// Screen switching functions (called from auth.js and event listeners)
// =========================================================================

function switchToRegister() {
    document.getElementById('login-form').classList.remove('active');
    document.getElementById('register-form').classList.add('active');
}

function switchToLogin() {
    document.getElementById('register-form').classList.remove('active');
    document.getElementById('login-form').classList.add('active');
}

function switchToAuthScreen() {
    document.getElementById('auth-screen').classList.add('active');
    document.getElementById('game-screen').classList.remove('active');
    
    // Clear forms
    document.getElementById('reg-username').value = '';
    document.getElementById('reg-display-name').value = '';
    document.getElementById('reg-class').value = 'adventurer';
    
    // Show welcome state
    document.getElementById('login-form').classList.add('active');
    document.getElementById('register-form').classList.remove('active');
}

function switchToGameScreen() {
    document.getElementById('auth-screen').classList.remove('active');
    document.getElementById('game-screen').classList.add('active');
    
    // Update player info
    updatePlayerInfo();
}

function updatePlayerInfo() {
    const user = authManager.getCurrentUser();
    if (!user) return;

    document.getElementById('player-name').textContent = user.first_name || user.username;
    document.getElementById('player-level').textContent = user.level || 1;
    document.getElementById('player-exp').textContent = user.experience || 0;
    document.getElementById('player-coins').textContent = user.coins || 0;
}

// =========================================================================
// Event listeners — bound after DOM is ready
// =========================================================================

document.addEventListener('DOMContentLoaded', function () {
    // "Create Character" button — shown by auth.js after Telegram session resolves
    const createButton = document.getElementById('create-character-button');
    if (createButton) {
        createButton.addEventListener('click', switchToRegister);
    }

    // "Enter the Realm" (register confirmation)
    const registerButton = document.getElementById('register-button');
    if (registerButton) {
        registerButton.addEventListener('click', registerUser);
    }

    // "Back" button (from register form to welcome/login)
    const backButton = document.getElementById('back-button');
    if (backButton) {
        backButton.addEventListener('click', switchToLogin);
    }

    // "Logout" button (game screen)
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }

    // Keyboard shortcuts — Enter triggers registration when on the register form
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            const authScreen = document.getElementById('auth-screen');
            if (authScreen && authScreen.classList.contains('active')) {
                const registerForm = document.getElementById('register-form');
                if (registerForm && registerForm.classList.contains('active')) {
                    registerUser();
                }
            }
        }
    });
});
