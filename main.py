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
            # Share one database session with the current update handler.
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception:
                # Roll back failed handler changes before passing the error up.
                session.rollback()
                raise


def init_db():
    """Initialize database"""
    # Create tables from SQLAlchemy models if they do not exist yet.
    Base.metadata.create_all(bind=engine)
    # Apply Alembic migrations (безпечні DDL замість сирого SQL)
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config('alembic.ini')
    command.upgrade(alembic_cfg, 'head')




async def set_bot_commands():
    """Set bot commands"""
    # Register the commands shown in the Telegram bot menu.
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
