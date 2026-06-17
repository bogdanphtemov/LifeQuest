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
    data = await state.get_data()
    authenticated_user_id = data.get("authenticated_user_id")

    if not authenticated_user_id:
        await message.answer("Please log in first with /start or /login.")
        return

    user = session.execute(
        select(User).where(User.id == authenticated_user_id)
    ).scalar_one_or_none()

    if not user or user.telegram_id != message.from_user.id:
        await state.clear()
        await message.answer("Session expired. Please log in again with /start.")
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
