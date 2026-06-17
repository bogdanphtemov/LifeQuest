# TG BOT RPG

Telegram бот для геіміфікації процесу самороз витку в піксельному стилі RPG формату.

## Опис проекту

**TG BOT RPG** — це інноваційна програма для мотивації саморозвитку, яка працює повністю на довірі користувача. Бот дозволяє користувачам:

- ✨ Створювати власні квести та визначати винагороду
- 🎮 Розвивати персонажа в пікселевому світі
- 💰 Заробляти монети та досвід
- 🏆 Проходити боси та розблоковувати нові локації
- 🛍️ Купувати косметичні товари та предмети

## Переваги

1. **Легкий доступ** — просто знайти бота в Telegram, не потрібно скачувати додаткову програму
2. **Широка аудиторія** — працює на Telegram, який є практично в кожного
3. **Повна свобода** — користувачі самі розробляють свої квести під свої потреби
4. **Вільний проект** — безкоштовний, відкритий, з можливістю долучитися до розробки

## Встановлення

### Вимоги
- Python 3.10+
- Telegram токен бота

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
```
Use your own token from [@BotFather](https://t.me/BotFather). Do not paste the real token into source files, README, issues, commits, or pull requests.

5. Run the bot:
```bash
python main.py
```

## Project Structure

```
TG_BOT_RPG/
├── main.py              # Application entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── .env.example         # Configuration example
├── .gitignore           # Files to ignore from version control
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
- **aiosqlite** - Asynchronous SQLite driver

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
