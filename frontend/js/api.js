/* API Communication Module */

const API_BASE_URL = window.location.protocol === 'file:'
    ? 'http://localhost:5000/api'
    : `${window.location.origin}/api`;

class APIClient {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

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

    // Auth endpoints
    async telegramSession(initData) {
        return this.request('/auth/telegram/session', {
            method: 'POST',
            body: JSON.stringify({
                init_data: initData,
            }),
        });
    }

    async telegramRegister(initData, username, displayName, characterClass = 'adventurer') {
        return this.request('/auth/telegram/register', {
            method: 'POST',
            body: JSON.stringify({
                init_data: initData,
                username,
                display_name: displayName,
                character_class: characterClass,
                avatar: 'pixel_adventurer',
            }),
        });
    }

    async register(username, password, telegramId, firstName = '', lastName = '') {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify({
                username,
                password,
                telegram_id: telegramId,
                first_name: firstName,
                last_name: lastName,
            }),
        });
    }

    async login(username, password, telegramId) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({
                username,
                password,
                telegram_id: telegramId,
            }),
        });
    }

    async getUser(telegramId) {
        return this.request(`/auth/user/${telegramId}`);
    }

    // Health check
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL.replace('/api', '')}/api/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
}

// Global API client
const api = new APIClient();
