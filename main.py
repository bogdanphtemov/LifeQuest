import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_bot_commands():
    """Set bot commands"""
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="profile", description="View profile"),
        BotCommand(command="help", description="Get help"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Main function"""
    logger.info("Bot is starting...")
    
    try:
        # Set bot commands
        await set_bot_commands()
        
        # Register command handlers here
        # from handlers import start, profile
        # dp.include_router(start.router)
        # dp.include_router(profile.router)
        
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
