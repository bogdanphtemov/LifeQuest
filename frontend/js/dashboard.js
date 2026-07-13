/* LifeQuest Dashboard Module
 *
 * Flow:
 *   1. Start Screen (animated pixel scene) is shown on load.
 *   2. Player clicks the animated "Start" signboard.
 *   3. System checks if a Telegram character exists.
 *   4. If registered — show Character Dashboard.
 *   5. If NOT registered — show Error screen with instructions.
 *   6. If Telegram context is missing — show offline message.
 */

// =========================================================================
// State
// =========================================================================

let isProcessing = false;

// =========================================================================
// Screen switching
// =========================================================================

function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(function (screen) {
        screen.classList.remove('active');
    });
}

function showScreen(screenId) {
    hideAllScreens();
    var el = document.getElementById(screenId);
    if (el) el.classList.add('active');
}

function showDashboard(user) {
    showScreen('dashboard-screen');

    document.getElementById('player-name').textContent =
        user.display_name || user.username || '—';
    document.getElementById('player-login').textContent =
        user.username || '—';
    document.getElementById('player-class').textContent =
        user.character_class || 'Adventurer';
    document.getElementById('player-avatar').textContent =
        user.avatar || 'pixel_adventurer';
    document.getElementById('player-level').textContent =
        user.level ?? '—';
    document.getElementById('player-exp').textContent =
        user.experience ?? '—';
    document.getElementById('player-coins').textContent =
        user.coins ?? '—';
}

function showNotRegistered(message) {
    showScreen('error-screen');

    var msgEl = document.getElementById('error-message');
    if (message && msgEl) {
        msgEl.textContent = message;
    }
}

// =========================================================================
// Character existence check (placeholder)
// =========================================================================

/**
 * checkCharacterExistence
 * Placeholder for the backend check. Currently uses the Telegram session API.
 *
 * @returns {Promise<{exists: boolean, user: object|null}>}
 */
async function checkCharacterExistence() {
    var tg = window.Telegram && window.Telegram.WebApp
        ? window.Telegram.WebApp
        : null;

    if (!tg || !tg.initData) {
        return {
            exists: false,
            user: null,
            error: 'Open this app from the Telegram bot to see your character.'
        };
    }

    tg.ready();
    tg.expand();

    try {
        var response = await api.telegramSession(tg.initData);

        if (response.registered && response.user) {
            return { exists: true, user: response.user };
        } else {
            return {
                exists: false,
                user: null,
                error: 'You do not have a character yet. ' +
                       'Open the Telegram bot and use /start to create one!'
            };
        }
    } catch (error) {
        console.error('Character check error:', error);
        return {
            exists: false,
            user: null,
            error: 'Could not verify your Telegram session. ' +
                   'Please open the bot with /start first.'
        };
    }
}

// =========================================================================
// Start button handler
// =========================================================================

function onStartClick() {
    if (isProcessing) return;
    isProcessing = true;

    var startBtn = document.getElementById('start-button');
    if (startBtn) {
        startBtn.style.animationPlayState = 'paused';
        startBtn.classList.add('start-sign-swing-paused');
    }

    // Call the character existence check
    checkCharacterExistence().then(function (result) {
        if (result.exists && result.user) {
            // Character exists → show Dashboard
            showDashboard(result.user);
        } else {
            // No character → show Error screen with message
            showNotRegistered(result.error);
        }
        isProcessing = false;
    }).catch(function (err) {
        console.error('Start flow error:', err);
        showNotRegistered('An unexpected error occurred. Please try again.');
        isProcessing = false;
    });
}

// =========================================================================
// Bootstrap
// =========================================================================

function init() {
    var startBtn = document.getElementById('start-button');
    if (startBtn) {
        startBtn.addEventListener('click', onStartClick);
        startBtn.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onStartClick();
            }
        });
    }

    // Pre-initialise Telegram WebApp (expand, ready)
    var tg = window.Telegram && window.Telegram.WebApp
        ? window.Telegram.WebApp
        : null;
    if (tg) {
        tg.ready();
        tg.expand();
    }
}

// Initialise after DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
