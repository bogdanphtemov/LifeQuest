import asyncio
import logging
from sqlalchemy import create_engine, inspect, text
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import BotCommand, Update
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.orm import Session, sessionmaker
from config import BOT_TOKEN, DATABASE_URL
from database.users import Base
from handlers import profile, start
from typing import Any, Callable, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database engine and session maker
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class DatabaseMiddleware(BaseMiddleware):
    """Middleware to inject database session into handlers"""
    
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Any],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        with SessionLocal() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                session.rollback()
                raise


def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)
    migrate_sqlite_schema()


def migrate_sqlite_schema():
    """Add missing SQLite columns for local development databases."""
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("users")}
    migrations = {
        "password_hash": "ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)",
        "display_name": "ALTER TABLE users ADD COLUMN display_name VARCHAR(255)",
        "avatar": (
            "ALTER TABLE users ADD COLUMN avatar VARCHAR(64) "
            "DEFAULT 'pixel_adventurer'"
        ),
        "character_class": (
            "ALTER TABLE users ADD COLUMN character_class VARCHAR(64) "
            "DEFAULT 'adventurer'"
        ),
    }

    with engine.begin() as connection:
        for column_name, statement in migrations.items():
            if column_name not in existing_columns:
                connection.execute(text(statement))


async def set_bot_commands():
    """Set bot commands"""
    commands = [
        BotCommand(command="start", description="Open the LifeQuest app"),
        BotCommand(command="login", description="Legacy chat login"),
        BotCommand(command="profile", description="View profile"),
        BotCommand(command="delete_account", description="Delete account"),
        BotCommand(command="cancel", description="Cancel current action"),
        BotCommand(command="help", description="Get help"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main function"""
    logger.info("Bot is starting...")
    
    try:
        # Initialize database
        init_db()
        logger.info("Database initialized")
        
        # Set bot commands
        await set_bot_commands()
        
        # Register middleware
        dp.update.middleware(DatabaseMiddleware())
        
        # Register command handlers
        dp.include_router(start.router)
        dp.include_router(profile.router)
        
        logger.info("Bot started. Waiting for messages...")
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
