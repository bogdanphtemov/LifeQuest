# TG BOT RPG

Telegram bot for gamifying self-development in a pixel-style RPG format.

## Project Description

**TG BOT RPG** is an innovative self-development motivation project built around user trust. The bot allows users to:

- ✨ Create custom quests and define rewards
- 🎮 Develop a character in a pixel world
- 💰 Earn coins and experience
- 🏆 Defeat bosses and unlock new locations
- 🛍️ Buy cosmetic goods and items

## Benefits

1. **Easy access** - just find the bot in Telegram; no extra app download is required.
2. **Broad audience** - runs on Telegram, a platform many users already have.
3. **Full freedom** - users design quests around their own goals and needs.
4. **Open project** - free, open, and welcoming to contributors.

## Installation

### Requirements
- Python 3.10+
- Telegram bot token

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TG_BOT_RPG.git
cd TG_BOT_RPG
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure `.env` file:
```bash
cp .env.example .env
```
Add your Telegram token to the `.env` file:
```
BOT_TOKEN=your_telegram_bot_token_here
WEB_APP_URL=http://localhost:5000
```
Use your own token from [@BotFather](https://t.me/BotFather). Do not paste the real token into source files, README, issues, commits, or pull requests.

For a real Telegram Mini App, `WEB_APP_URL` must be a public HTTPS URL. For local testing, run the Flask server and expose it with a tunnel such as ngrok or cloudflared, then set `WEB_APP_URL` to that HTTPS address.

5. Run the web/API server:
```bash
python3 backend/app.py
```

The web app will be available at `http://localhost:5000`.

6. In another terminal, run the Telegram bot:
```bash
python3 main.py
```

## Project Structure

```
TG_BOT_RPG/
├── main.py              # Application entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Configuration example
├── .gitignore           # Files to ignore from version control
├── backend/             # Flask API and Mini App hosting
│   ├── app.py           # Web/API server
│   └── routes/          # API routes
├── frontend/            # Telegram Mini App frontend
│   ├── index.html       # App shell
│   ├── css/             # Pixel RPG styling
│   └── js/              # API, auth, and UI logic
├── handlers/            # Bot command handlers
│   ├── start.py         # /start command
│   └── profile.py       # User profile
├── database/            # Database operations
│   └── users.py         # User model
└── assets/              # Graphic resources
```

## Dependencies

- **aiogram** - Framework for working with Telegram API
- **python-dotenv** - Environment variables management
- **SQLAlchemy** - ORM for database operations
- **Flask** - Web/API server for the Telegram Mini App
- **Flask-Cors** - CORS support for the API

## Security

⚠️ **IMPORTANT**: Never commit your `.env` file with the token. The repository contains only `.env.example`, which is a safe template without real secrets.

Security rules for contributors:

- Keep real secrets only in local `.env` files or in your hosting provider's secret manager.
- Do not hardcode `BOT_TOKEN` in Python files.
- Do not send tokens in screenshots, GitHub Issues, Pull Requests, logs, or chat messages.
- If a token was accidentally published, revoke it immediately in [@BotFather](https://t.me/BotFather) and generate a new one.
- For GitHub Actions or deployments, store tokens in GitHub repository secrets, for example `BOT_TOKEN`, and pass them as environment variables.
- Everyone who forks the project should create their own bot token. Shared production tokens should not be used for local development.

## License

MIT License - feel free to use it for your projects!

## Contributing

Welcome to development! If you have ideas or found a bug, please create an Issue or Pull Request.

## Contact

If you have questions, please contact the project developer.

---

Happy coding! 🚀
