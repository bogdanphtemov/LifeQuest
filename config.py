import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists.
load_dotenv()

TOKEN_PLACEHOLDERS = {
    "",
    "your_telegram_bot_token_here",
    "change_me",
    "replace_me",
}


def get_required_secret(name: str) -> str:
    """Read a required secret from environment variables."""
    value = os.getenv(name, "").strip()

    if value in TOKEN_PLACEHOLDERS:
        raise ValueError(
            f"{name} is not configured. Copy .env.example to .env and set a real value."
        )

    return value


# Telegram Bot Token
BOT_TOKEN = get_required_secret("BOT_TOKEN")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bot.db")

# Other settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
