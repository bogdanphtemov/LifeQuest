from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.users import User

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: types.Message, state: FSMContext, session: Session):
    """Handle /profile command"""
    user = session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    ).scalar_one_or_none()

    if not user:
        await message.answer("Open the app with /start and create your character first.")
        return

    await message.answer(
        "Your Profile\n\n"
        f"Name: {user.display_name or user.username}\n"
        f"Login: {user.username}\n"
        f"Class: {user.character_class}\n"
        f"Avatar: {user.avatar}\n"
        f"Level: {user.level}\n"
        f"XP: {user.experience}\n"
        f"Coins: {user.coins}"
    )
