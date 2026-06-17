from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handle /start command"""
    await message.answer(
        "Welcome to TG BOT RPG! 🎮\n\n"
        "This is a gamified self-development experience.\n"
        "Enter /profile to view your profile"
    )
