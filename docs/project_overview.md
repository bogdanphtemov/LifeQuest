# LifeQuest — Project Overview

> **Disclaimer for AI assistants:** This document is a single source of truth.  
> If you are an AI agent reading this, treat every section as authoritative.  
> Before making any changes, re-read the relevant sections to preserve architectural consistency.

---

## 1. General Idea

**LifeQuest** is a gamified habit tracker / RPG-style life management app that runs as a **Telegram Mini App** (TMA).  
Users interact with a Telegram bot to manage their character (create, level up, earn coins, complete quests), and the **Mini App (frontend)** serves as a **read-only dashboard** — displaying user stats, character info, and progress.

The app is a **single-page application** (SPA) with 3 screens (loading, dashboard, error).  
The backend is a **Flask** server that provides a **REST API** (JSON) and works with a **PostgreSQL** database.

---

## 2. Main Goal

Provide a seamless, gamified experience where:

- A **Telegram bot** handles all character management (registration, quests, inventory, etc.).
- A **Telegram Mini App** (this frontend) displays a **character dashboard** with stats (level, XP, coins, class, avatar).
- Users open the Mini App from the bot to **view** their progress — no editing is done inside the Mini App.
- The app authenticates users automatically via **Telegram initData** (no manual login needed for TMA users).

---

## 3. User Interaction Flow

```
                        ┌─────────────────────────────┐
                        │    Telegram Bot (chat)       │
                        │   - /start → registration    │
                        │   - /profile → view stats    │
                        │   - /quests → manage tasks   │
                        └──────────┬──────────────────┘
                                   │ opens via inline button / menu button
                                   ▼
            ┌───────────────────────────────────────────┐
            │         Telegram Mini App (frontend)      │
            │                                           │
            │  1. Page load                              │
            │  2. Read Telegram.WebApp.initData          │
            │  3. Send initData to backend for verify    │
            │  4. Backend responds:                      │
            │     a) registered=true → show dashboard    │
            │     b) registered=false → show error       │
            │        screen with "create character" msg  │
            └───────────────────────────────────────────┘
```

**Detailed steps:**

1. User taps a button inside the Telegram bot → Telegram opens the Mini App URL.
2. Telegram injects `window.Telegram.WebApp` with an `initData` string (signed HMAC payload).
3. `dashboard.js` → `loadCharacterDashboard()` fires on `window.load`:
   - Checks `Telegram.WebApp` exists & has `initData`.
   - Calls `tg.ready()` and `tg.expand()`.
   - Sends `POST /api/auth/telegram/session` with `init_data`.
4. Backend validates the HMAC signature, looks up the user by `telegram_id`.
5. **If registered:** `showDashboard(user)` — fills stat fields from backend response.
6. **If NOT registered:** `showNotRegistered()` — shows error screen with instructions to use `/start` in the bot.
7. **If initData missing:** Same error screen with "open from bot" message.

---

## 4. Screen List

### 4.1 Loading Screen (`#loading-screen`)
- **Status:** Always active on startup (CSS class `.active`).
- **Content:** Pixel-art landscape background (sky, sun, clouds, hills, village, windmill, wheat field, walking characters), a wooden hanging sign with "LIFE QUEST" title and a loading text (`<p id="loading-text">`).
- **Purpose:** Shown while the app verifies the Telegram session.
- **Transition:** Replaced by dashboard or error screen after the API responds.

### 4.2 Dashboard Screen (`#dashboard-screen`)
- **Status:** Shown when user is registered.
- **Content:** Same pixel-art background (simplified — sky, sun, clouds, hills), a wooden sign with:
  - "⚔️ LIFE QUEST" title
  - Character card with fields: **Name, Login, Class, Avatar, Level, Experience, Coins**.
  - A note: "Data is pulled from your Telegram character. Use the bot to manage your adventure."
- **Data source:** Backend response from session endpoint (or `/auth/user/:id`).

### 4.3 Error / Not Registered Screen (`#error-screen`)
- **Status:** Shown when user is not registered or when session resolution fails.
- **Content:** Same simplified pixel-art background, wooden sign with:
  - "NO CHARACTER" title
  - Error message: "You don't have a character yet. Open the Telegram bot and use /start to create one!"
- **Purpose:** Guides the user back to the bot for registration.

---

## 5. Screen Transition Map

```
                    ┌───────────────────┐
                    │   Loading Screen   │  ← always active on page load
                    │  (splash + check)  │
                    └────────┬──────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
         session valid?              session invalid?
                │                         │
                ▼                         ▼
    ┌─────────────────────┐   ┌──────────────────────┐
    │   Dashboard Screen  │   │   Error Screen        │
    │  (registered user)  │   │  (not registered /    │
    │                     │   │   session failed)     │
    └─────────────────────┘   └──────────────────────┘
```

**Rules:**

- Only **one** screen can have the class `.active` at any time.
- Switching is done via:
  ```js
  hideAllScreens();                       // removes .active from all .screen elements
  document.getElementById('target').classList.add('active');
  ```
- No navigation buttons, no back/forward flow — the SPA is purely reactive to the session state.
- To re-check the session, the user must reload the Mini App.

---

## 6. Module Map (Frontend)

| # | File | Role | Key Exports / Globals | Dependencies |
|---|------|------|-----------------------|--------------|
| 1 | `frontend/index.html` | Entry point, screen markup (3 screens), script loader | — | Loads `api.js` then `dashboard.js` |
| 2 | `frontend/js/api.js` | **API client** – wraps `fetch()` for all backend calls | `class APIClient`, singleton `const api` | None (standalone) |
| 3 | `frontend/js/dashboard.js` | **Controller + View** – orchestrates session check, renders screens | `loadCharacterDashboard()`, `showDashboard()`, `showNotRegistered()`, `hideAllScreens()`, `updateLoadingText()` | Depends on `api.js` (`api.telegramSession`) |
_Note: `auth.js` and `ui.js` exist in the frontend/js/ directory but are legacy/unused and are NOT loaded in production._

### 6.1 Module Dependency Graph

```
index.html
  ├── telegram-web-app.js  (CDN, injects window.Telegram.WebApp)
  ├── js/api.js            (pure HTTP client)
  └── js/dashboard.js      (controller + view, depends on api.js)
```

---

## 7. Data Flow & Data Structures

### 7.1 API Request/Response

**Endpoint:** `POST /api/auth/telegram/session`

**Request body:**
```json
{
  "init_data": "query_id=...&auth_date=...&hash=..."
}
```

**Response (registered):**
```json
{
  "status": "ok",
  "registered": true,
  "telegram_user": {
    "id": 123456789,
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "language_code": "en"
  },
  "user": {
    "id": 1,
    "telegram_id": 123456789,
    "username": "johndoe",
    "display_name": "John Doe",
    "character_class": "adventurer",
    "avatar": "pixel_adventurer",
    "level": 5,
    "experience": 1200,
    "coins": 350,
    "created_at": "2025-01-01T00:00:00Z"
  }
}
```

**Response (not registered):**
```json
{
  "status": "ok",
  "registered": false,
  "telegram_user": { "id": 123456789, ... },
  "user": null
}
```

**Other endpoints:**

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/auth/user/:telegramId` | Fetch user profile by Telegram ID |
| GET | `/api/health` | Health check |

_Note: The `/api/auth/telegram/register`, `/api/auth/register`, and `/api/auth/login` endpoints were removed_ 
_during the simplification pass (registration now happens exclusively in the Telegram bot)._

### 7.2 Frontend Data Flow

```
Telegram.WebApp.initData (string)
        │
        ▼
  api.telegramSession(initData)     ← in dashboard.js
        │
        ▼
  POST /api/auth/telegram/session    ← backend Flask route
        │
        ▼
  response JSON
        │
        ├── registered=true  →  showDashboard(response.user)
        │                        Populates DOM elements:
        │                        #player-name     ← user.display_name || user.username
        │                        #player-login    ← user.username
        │                        #player-class    ← user.character_class
        │                        #player-avatar   ← user.avatar
        │                        #player-level    ← user.level
        │                        #player-exp      ← user.experience
        │                        #player-coins    ← user.coins
        │
        └── registered=false →  showNotRegistered()
                                Shows #error-screen with default message
```

### 7.3 Database Schema (Users Table)

From `alembic/versions/ffb10ecdf575_initial_users_table.py`:

| Column | Type | Notes |
|--------|------|-------|
| `id` | Integer (PK) | Auto-increment |
| `telegram_id` | BigInt (unique, nullable) | Telegram user ID; nullable for legacy password users |
| `username` | String(32) (unique, not null) | Login name |
| `display_name` | String(64) (nullable) | Hero name shown in dashboard |
| `password_hash` | String(128) (nullable) | PBKDF2-HMAC-SHA256; null for Telegram-only accounts |
| `character_class` | String(20) (default='adventurer') | RPG class (adventurer, warrior, mage, ranger) |
| `avatar` | String(64) (default='pixel_adventurer') | Avatar identifier |
| `level` | Integer (default=1) | Current level |
| `experience` | Integer (default=0) | Total XP |
| `coins` | Integer (default=0) | Currency |
| `created_at` | DateTime | Auto set on creation |

---

## 8. Backend Architecture

### 8.1 Structure

```
backend/
  __init__.py           ← Flask app factory
  app.py                ← app entry point, blueprint registration, DB init
  routes/
    __init__.py         ← blueprint definitions
    auth_routes.py      ← /api/auth/* routes (session, account, user)

database/
  __init__.py           ← SQLAlchemy init
  users.py              ← User model (SQLAlchemy ORM)

config.py               ← App configuration (env vars, secrets)
main.py                 ← Telegram bot entry point (aiogram)
handlers/               ← Telegram bot handlers
  __init__.py
  profile.py
  start.py
```

_Note: alembic/ directory exists but is not critical — the current `app.py` uses
automatic schema creation (`Base.metadata.create_all`) and additive SQLite migrations
for local development._

### 8.2 Current Backend Routes

Only three API routes remain active:

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/auth/telegram/session` | Verify Telegram initData, check registration status |
| DELETE | `/api/auth/account` | Delete account (telegram_id + password confirmation) |
| GET | `/api/auth/user/:telegramId` | Fetch user profile by Telegram ID |
| GET | `/api/health` | Server health check |

_All password-based registration/login routes were removed when the project
was simplified to bot-only registration._

### 8.3 Key Backend Behaviours

- **initData validation:** The backend verifies the HMAC-SHA256 signature of `init_data` using the Bot Token as the secret key. If invalid, the request is rejected.
- **Session resolution:** After validation, the backend looks up `telegram_id` in the `users` table. Returns `registered: true/false` + user data if found.
- **Error responses:** Always return JSON with at least `{"status": "error", "message": "..."}`.

---

## 9. Recommended Architecture (for future development)

### 9.1 Separation of Concerns

Current code mixes API calls, platform code (`Telegram.WebApp`), and UI rendering in a single file (`dashboard.js`).  
For maintainability, split into three layers:

```
┌─────────────────────────────────────────────────┐
│                  session.js                      │
│   (orchestrator — calls api, returns result)    │
│   - resolveSession()                             │
│   - knows about Telegram.WebApp                  │
│   - does NOT know about DOM                      │
└───────────────────────┬─────────────────────────┘
                        │ depends on
                        ▼
┌─────────────────────────────────────────────────┐
│                   api.js                         │
│   (pure HTTP client — fetch wrapper)            │
│   - class APIClient { request(), endpoints… }   │
│   - knows NOTHING about Telegram or DOM         │
└─────────────────────────────────────────────────┘
                        ▲ depends on
┌─────────────────────────────────────────────────┐
│                dashboard.js                      │
│   (pure UI layer — DOM rendering)               │
│   - showDashboard(user)                          │
│   - showNotRegistered(msg)                       │
│   - hideAllScreens()                             │
│   - does NOT call api directly                   │
└─────────────────────────────────────────────────┘
```

### 9.2 Guidelines

1. **api.js** should remain a **pure HTTP client** — no platform checks, no DOM access.
2. **dashboard.js** should be a **pure UI module** — only DOM manipulation, no API calls, no Telegram platform code.
3. A new **session.js** (or keep in dashboard.js as a separate function) acts as the **orchestrator** — calls API, processes results, delegates to UI.
4. Never mix concerns in a single function.

### 9.3 Script Load Order

```
api.js → session.js → dashboard.js
```

Each module should be independently testable. Functions should accept parameters rather than reading global state.

---

## 10. Key Files Reference

| File | Purpose |
|------|---------|
| `frontend/index.html` | SPA markup with 3 screens, loads scripts |
| `frontend/css/main.css` | Base layout styles |
| `frontend/css/pixel-fonts.css` | Pixel/retro font definitions |
| `frontend/css/pixel-scene.css` | Pixel-art animated background |
| `frontend/css/dark-fantasy.css` | Dark fantasy theme overrides |
| `frontend/js/api.js` | API client singleton |
| `frontend/js/dashboard.js` | Main controller + UI (session check, render) |
| `frontend/js/auth.js` | Legacy auth functions (unused in production) |
| `frontend/js/ui.js` | Legacy UI logic (unused in production) |
| `backend/app.py` | Flask application factory |
| `backend/routes/auth_routes.py` | All /api/auth/* endpoints |
| `database/users.py` | User SQLAlchemy model |
| `config.py` | App configuration (env, secrets, DB URL) |
| `main.py` | WSGI entry point |
| `handlers/start.py` | Telegram bot /start handler |
| `handlers/profile.py` | Telegram bot profile handler |
| `alembic/versions/ffb10ecdf575_initial_users_table.py` | DB migration |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

---

## 11. Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend (SPA) | Vanilla JS, CSS3, HTML5 |
| Backend (API) | Python 3, Flask |
| Database | PostgreSQL (via SQLAlchemy ORM) |
| Migrations | Alembic |
| Telegram Integration | `telegram-web-app.js` (CDN) + Telegram Bot API |
| Authentication | HMAC-SHA256 (initData verification), PBKDF2 (legacy passwords) |
| Bot Framework | aiogram / python-telegram-bot (handlers) |

---

## 12. Common Pitfalls (for AI agents)

1. **Do not add new screens without updating the screen transition map.**
2. **Do not mix API calls with DOM manipulation** — keep `api.js` pure.
3. **`auth.js` and `ui.js` exist but are NOT loaded in production HTML** — do not import them in new code unless you also update `index.html`.
4. **Only one screen can have `.active`** — always call `hideAllScreens()` before showing a new screen.
5. **initData is the single source of truth** for Telegram authentication — never ask for username/password inside the Mini App.
6. **Backend returns `status: "ok"` or `status: "error"`** — always check this before using the `user` object.
