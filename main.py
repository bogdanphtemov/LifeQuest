import asyncio
import logging
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.types import BotCommand, Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import BOT_TOKEN, DATABASE_URL
from database.users import Base
from handlers import start
from typing import Any, Callable, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Convert sqlite:// to sqlite+aiosqlite:// for async
async_db_url = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

# Create async engine and session maker
engine = create_async_engine(async_db_url, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

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
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)


async def init_db():
    """Initialize database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def set_bot_commands():
    """Set bot commands"""
    commands = [
        BotCommand(command="start", description="Start the bot and register"),
        BotCommand(command="profile", description="View profile"),
        BotCommand(command="help", description="Get help"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main function"""
    logger.info("Bot is starting...")
    
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized")
        
        # Set bot commands
        await set_bot_commands()
        
        # Register middleware
        dp.update.middleware(DatabaseMiddleware())
        
        # Register command handlers
        dp.include_router(start.router)
        
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
