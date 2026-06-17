/* UI Management Module */

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
    document.getElementById('login-username').value = '';
    document.getElementById('reg-username').value = '';
    document.getElementById('reg-password').value = '';
    document.getElementById('reg-first-name').value = '';
    document.getElementById('reg-last-name').value = '';
    
    // Show login form
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

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const authScreen = document.getElementById('auth-screen');
        if (authScreen.classList.contains('active')) {
            const loginForm = document.getElementById('login-form');
            const registerForm = document.getElementById('register-form');
            
            if (loginForm.classList.contains('active')) {
                loginUser();
            } else if (registerForm.classList.contains('active')) {
                registerUser();
            }
        }
    }
});
