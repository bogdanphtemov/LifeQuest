/**
 * LifeQuest — UI module.
 *
 * Manages the DOM rendering: loading state, registered/dashboard state,
 * not-registered state, and the delete-account confirmation flow.
 *
 * Relies on auth.js for API calls.
 */

// ---------------------------------------------------------------------------
// DOM references (cached once on first render)
// ---------------------------------------------------------------------------

let els = {};

function cacheElements() {
    els = {
        loading: document.getElementById('loading'),
        notRegistered: document.getElementById('not-registered'),
        authenticated: document.getElementById('authenticated'),
        deleteModal: document.getElementById('delete-modal'),

        profileName: document.getElementById('profile-name'),
        profileClass: document.getElementById('profile-class'),
        profileAvatar: document.getElementById('profile-avatar'),
        statLevel: document.getElementById('stat-level'),
        statExperience: document.getElementById('stat-experience'),
        statCoins: document.getElementById('stat-coins'),
        statUsername: document.getElementById('stat-username'),
        telegramInfo: document.getElementById('telegram-info'),

        retrySession: document.getElementById('retry-session'),
        refreshProfile: document.getElementById('refresh-profile'),
        deleteAccountBtn: document.getElementById('delete-account'),
        confirmDelete: document.getElementById('confirm-delete'),
        cancelDelete: document.getElementById('cancel-delete'),
        deletePassword: document.getElementById('delete-password'),
    };
}

// ---------------------------------------------------------------------------
// Application state
// ---------------------------------------------------------------------------

let currentTelegramUser = null;
let currentUser = null;

// ---------------------------------------------------------------------------
// View switching
// ---------------------------------------------------------------------------

function showView(viewId) {
    [els.loading, els.notRegistered, els.authenticated, els.deleteModal].forEach((el) => {
        if (el) el.classList.add('hidden');
    });
    const target = document.getElementById(viewId);
    if (target) target.classList.remove('hidden');
}

// ---------------------------------------------------------------------------
// Render profile / dashboard
// ---------------------------------------------------------------------------

function renderProfile(user, telegramUser) {
    if (!els.profileName) return;

    const classEmojis = {
        adventurer: '⚔️',
        warrior: '🛡️',
        mage: '🔮',
        ranger: '🏹',
    };

    const classEmoji = classEmojis[user.character_class] || '⚔️';
    const displayName = user.display_name || user.username || 'Player';
    const className = user.character_class
        ? `${classEmoji} ${user.character_class.charAt(0).toUpperCase() + user.character_class.slice(1)}`
        : '—';

    els.profileName.textContent = displayName;
    els.profileClass.textContent = `Class: ${className}`;
    els.profileAvatar.textContent = classEmoji;
    els.statLevel.textContent = user.level ?? '—';
    els.statExperience.textContent = user.experience ?? '—';
    els.statCoins.textContent = user.coins ?? '—';
    els.statUsername.textContent = `@${user.username ?? '—'}`;

    // Show Telegram info if available
    if (telegramUser && els.telegramInfo) {
        const parts = [];
        if (telegramUser.first_name) parts.push(telegramUser.first_name);
        if (telegramUser.last_name) parts.push(telegramUser.last_name);
        const name = parts.join(' ') || 'Telegram user';
        const lang = telegramUser.language_code
            ? ` (${telegramUser.language_code.toUpperCase()})`
            : '';
        els.telegramInfo.textContent = `👤 ${name}${lang}`;
    }
}

// ---------------------------------------------------------------------------
// Main app initialisation
// ---------------------------------------------------------------------------

async function initApp() {
    cacheElements();

    // Show loading
    showView('loading');

    try {
        const data = await resolveSession();

        if (data.status === 'success' && data.registered && data.user) {
            // Registered user — show dashboard
            currentTelegramUser = data.telegram_user;
            currentUser = data.user;
            renderProfile(currentUser, currentTelegramUser);
            showView('authenticated');
        } else {
            // Not registered — show "create in bot" screen
            showView('not-registered');
        }
    } catch (err) {
        console.error('Session resolution failed:', err);
        showView('not-registered');
    }
}

// ---------------------------------------------------------------------------
// Event listeners
// ---------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', () => {
    initApp();

    // Retry session (not-registered screen)
    const retryBtn = document.getElementById('retry-session');
    if (retryBtn) {
        retryBtn.addEventListener('click', () => initApp());
    }

    // Refresh profile (dashboard)
    const refreshBtn = document.getElementById('refresh-profile');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', async () => {
            if (!currentTelegramUser?.id) return;
            try {
                const data = await fetchUserProfile(currentTelegramUser.id);
                if (data.status === 'success' && data.user) {
                    currentUser = data.user;
                    renderProfile(currentUser, currentTelegramUser);
                }
            } catch (err) {
                console.error('Profile refresh failed:', err);
            }
        });
    }

    // Delete account button (dashboard)
    const deleteBtn = document.getElementById('delete-account');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', () => {
            if (els.deleteModal) {
                els.deleteModal.classList.remove('hidden');
                els.deletePassword.value = '';
                els.deletePassword.focus();
            }
        });
    }

    // Cancel delete
    const cancelBtn = document.getElementById('cancel-delete');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            if (els.deleteModal) els.deleteModal.classList.add('hidden');
        });
    }

    // Confirm delete
    const confirmBtn = document.getElementById('confirm-delete');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', async () => {
            const password = els.deletePassword?.value;
            const telegramId = currentTelegramUser?.id || currentUser?.telegram_id;

            if (!password || !telegramId) return;

            confirmBtn.disabled = true;
            confirmBtn.textContent = '⏳ Deleting...';

            try {
                const result = await deleteAccount(telegramId, password);
                if (result.status === 'success') {
                    alert('Account deleted successfully.');
                    currentTelegramUser = null;
                    currentUser = null;
                    showView('not-registered');
                } else {
                    alert('Error: ' + (result.message || 'Could not delete account.'));
                }
            } catch (err) {
                alert('Network error. Please try again.');
                console.error('Delete failed:', err);
            } finally {
                confirmBtn.disabled = false;
                confirmBtn.textContent = '🗑️ Confirm Delete';
                if (els.deleteModal) els.deleteModal.classList.add('hidden');
            }
        });
    }
});
