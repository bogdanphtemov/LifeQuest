/* LifeQuest Dashboard Module

   Simplified read-only dashboard for the Telegram Mini App.
   This replaces the old auth.js + ui.js combo.

   Flow:
   1. On page load, get Telegram.WebApp initData.
   2. Send initData to backend for verification (/api/auth/telegram/session).
   3. If user is registered -> show character stats.
   4. If user is NOT registered -> show error screen with instructions.
   5. If Telegram context is missing -> show offline message.
*/

// =========================================================================
// Dashboard initialisation
// =========================================================================

async function loadCharacterDashboard() {
    const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;

    if (!tg || !tg.initData) {
        showNotRegistered(
            'Open this app from the Telegram bot to see your character.'
        );
        return;
    }

    tg.ready();
    tg.expand();

    updateLoadingText('Verifying your identity...');

    try {
        const response = await api.telegramSession(tg.initData);

        if (response.registered && response.user) {
            showDashboard(response.user);
        } else {
            showNotRegistered();
        }
    } catch (error) {
        console.error('Dashboard load error:', error);
        showNotRegistered(
            'Could not verify your Telegram session. ' +
            'Please open the bot with /start first.'
        );
    }
}

// =========================================================================
// Screen switching
// =========================================================================

function showDashboard(user) {
    hideAllScreens();
    document.getElementById('dashboard-screen').classList.add('active');

    document.getElementById('player-name').textContent =
        user.display_name || user.username || '—';
    document.getElementById('player-login').textContent =
        user.username || '—';
    document.getElementById('player-class').textContent =
        user.character_class || 'adventurer';
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
    hideAllScreens();
    document.getElementById('error-screen').classList.add('active');

    if (message) {
        document.getElementById('error-message').textContent = message;
    }
}

function updateLoadingText(text) {
    const el = document.getElementById('loading-text');
    if (el) el.textContent = text;
}

function hideAllScreens() {
    document.querySelectorAll('.screen').forEach(function (screen) {
        screen.classList.remove('active');
    });
}

// =========================================================================
// Bootstrap
// =========================================================================

window.addEventListener('load', loadCharacterDashboard);
