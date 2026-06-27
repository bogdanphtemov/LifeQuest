/**
 * LifeQuest — authentication module.
 *
 * Handles the Telegram Mini App session lifecycle:
 * 1. On load, reads initData from Telegram.WebApp.
 * 2. Sends it to POST /api/auth/telegram/session (backend).
 * 3. Based on the response, either shows the game screen or a
 *    "not registered" screen prompting the user to create a character in the bot.
 */

const API_BASE = '/api/auth';

/**
 * Resolve the current Telegram session.
 *
 * Makes a POST request to the backend with the Telegram initData.
 * The backend verifies the signature, looks up the user, and returns
 * whether the user is registered.
 *
 * @returns {Promise<{status: string, registered: boolean, telegram_user: object|null, user: object|null}>}
 */
async function resolveSession() {
    const initData = window.Telegram?.WebApp?.initData;

    if (!initData) {
        // Running outside Telegram or initData is missing — return unregistered.
        return { status: 'error', registered: false, telegram_user: null, user: null };
    }

    const response = await fetch(`${API_BASE}/telegram/session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ init_data: initData }),
    });

    return response.json();
}

/**
 * Delete the user account.
 *
 * @param {number} telegramId — the user's Telegram ID
 * @param {string} password — the user's password for confirmation
 * @returns {Promise<object>} the API response
 */
async function deleteAccount(telegramId, password) {
    const response = await fetch(`${API_BASE}/account`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ telegram_id: telegramId, password }),
    });
    return response.json();
}

/**
 * Fetch full user profile by telegram_id.
 *
 * @param {number} telegramId
 * @returns {Promise<object>} the API response
 */
async function fetchUserProfile(telegramId) {
    const response = await fetch(`${API_BASE}/user/${telegramId}`);
    return response.json();
}
