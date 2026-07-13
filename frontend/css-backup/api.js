/* API Communication Module

   Thin wrapper around the Fetch API for communicating with the LifeQuest
   Flask backend. Every network request flows through this module, keeping
   the frontend dashboard module (dashboard.js) free of raw fetch() calls.

   Architectural notes:
   - The base URL is determined at module load time based on the protocol.
     When the file is opened directly (file://), it defaults to a local dev
     server at localhost:5000. When served through a public HTTPS domain
     (Telegram Mini App), it uses the current origin.
   - Every response from the server is expected to be JSON with at minimum
     a "status" field ("ok" | "error"). Errors are thrown as JavaScript
     Error objects, leaving caller code to catch and display them.
   - The global singleton 'api' is used by dashboard.js; no other module
     needs direct access to the APIClient class.
   - Only the telegramSession() and healthCheck() methods are currently
     used by the simplified frontend. The other methods (register, login,
     getUser) are kept as legacy for future use.
*/

const API_BASE_URL = window.location.protocol === 'file:'
    ? 'http://localhost:5000/api'
    : `${window.location.origin}/api`;

class APIClient {
    /**
     * @param {string} baseURL - Root URL for all API requests (defaults to
     *     the module-level constant above). Kept as a parameter primarily
     *     for testability; production code uses the singleton.
     */
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

    /**
     * Core request dispatcher — used by every other method in this class.
     *
     * Flow:
     * 1. Concatenates the base URL with the endpoint path.
     * 2. Merges the caller's options (method, body, etc.) with the default
     *    JSON content-type header.
     * 3. Calls fetch() and parses the JSON response.
     * 4. If the HTTP status is not OK, throws an Error with the server's
     *    "message" field (or the status code as a fallback).
     * 5. Returns the parsed JSON on success.
     *
     * @param {string} endpoint - API path (e.g. "/auth/telegram/session").
     * @param {object} [options] - Fetch options (method, body, headers…).
     * @returns {Promise<object>} - JSON response body from the server.
     * @throws {Error} - On network failure or non-OK HTTP response.
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options,
        };

        try {
            const response = await fetch(url, defaultOptions);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || `HTTP ${response.status}`);
            }

            return data;
        } catch (error) {
            console.error(`API Error: ${error.message}`);
            throw error;
        }
    }

    // =====================================================================
    // Auth endpoints
    // =====================================================================

    /**
     * POST /api/auth/telegram/session
     *
     * Resolve the current Telegram Mini App session. This is the first call
     * made by the frontend after the Mini App opens. It validates the
     * Telegram initData on the server and returns whether the user has an
     * existing RPG character.
     *
     * @param {string} initData - Raw initData string from Telegram.WebApp.
     * @returns {Promise<object>} - { status, registered, telegram_user, user }.
     */
    async telegramSession(initData) {
        return this.request('/auth/telegram/session', {
            method: 'POST',
            body: JSON.stringify({
                init_data: initData,
            }),
        });
    }

    /**
     * GET /api/auth/user/:telegramId
     *
     * Fetch a user profile by Telegram ID. Used after session resolution
     * to load character data.
     *
     * @param {number} telegramId - Telegram user ID.
     * @returns {Promise<object>} - { status, user }.
     */
    async getUser(telegramId) {
        return this.request(`/auth/user/${telegramId}`);
    }

    // =====================================================================
    // Utility
    // =====================================================================

    /**
     * GET /api/health
     *
     * Simple connectivity check. Returns true when the server responds
     * with any OK status, false on any failure (network error, timeout,
     * non-OK status). Used by auth.js to detect whether the backend is
     * reachable before attempting a full session resolution.
     *
     * @returns {Promise<boolean>}
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api', '')}/api/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}

// Global singleton — used by auth.js for all backend communication.
const api = new APIClient();
