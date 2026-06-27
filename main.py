import asyncio
import logging
from sqlalchemy import create_engine
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import BotCommand, Update
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.orm import Session, sessionmaker
from config import BOT_TOKEN, DATABASE_URL
from database.users import Base
from handlers import profile, start
from typing import Any, Callable, Dict

def _setup_logging():
    """Configure root logger with our standard format.

    Extracted into a function so it can be called both at module load
    and after Alembic's fileConfig() resets the root logger.
    """
    # Remove any handlers that Alembic may have attached
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    root.addHandler(handler)


_setup_logging()
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
            # Share one database session with the current update handler.
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                # Roll back failed handler changes before passing the error up.
                session.rollback()
                raise


def init_db():
    """Initialize database using Alembic migrations.

    Alembic is the single source of truth for schema management.
    The migration chain (alembic/versions/) will create, alter, or
    skip tables as needed, so there is no need to call
    Base.metadata.create_all() beforehand.

    Warning: Alembic's env.py calls logging.config.fileConfig() which
    OVERWRITES the root logger with settings from alembic.ini (level=WARNING).
    We re-configure logging afterwards so that __main__ logs are visible.
    """
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, 'head')

    # Alembic's fileConfig() resets the root logger (level, handlers, formatter).
    # The disable_existing_loggers=False fix in alembic/env.py prevents existing
    # loggers from being silenced, but we still need to restore the root logger
    # to keep our own format and level after the migration completes.
    _setup_logging()




async def set_bot_commands():
    """Set bot commands"""
    # Register the commands shown in the Telegram bot menu.
    commands = [
        BotCommand(command="start", description="🚀 Start LifeQuest"),
        BotCommand(command="profile", description="👤 Character profile"),
        BotCommand(command="delete_account", description="🗑️ Delete account"),
        BotCommand(command="cancel", description="❌ Cancel action"),
        BotCommand(command="help", description="📋 Help"),
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
        # Start receiving updates until the process is stopped.
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        # Close the HTTP session opened by the bot client.
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
