from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Handle /profile command"""
    await message.answer(
        "👤 Your Profile:\n\n"
        "Coming soon during development..."
    )
