"""
Telegram bot handler for the /profile command.

This module provides a single handler that reads the authenticated user's RPG
character data from the database and formats it as a plain-text summary.

Module-level dependencies:
- router (aiogram.Router): Registered in main.py with dp.include_router().
- session (sqlalchemy.orm.Session): Injected by the DatabaseMiddleware (main.py).
- User (database.users): The SQLAlchemy model queried for profile data.
"""

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.users import User

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: types.Message, state: FSMContext, session: Session):
    """
    Handle the /profile command — display the user's RPG character summary.

    Flow:
    1. Look up the User row by the sender's Telegram ID.
    2. If no user is found, prompt the user to register via /start.
    3. Otherwise, format and send a text card with the user's RPG attributes:
       display name, login, character class, avatar, level, experience, and coins.

    Architectural notes:
    - The handler does NOT check FSM state for authentication markers.
      This means /profile works both for authenticated and unauthenticated sessions,
      as long as the Telegram ID is linked to a User record.
    - Profile display is read-only; all mutations happen through the Mini App or
      registration/login flows in handlers/start.py.
    """
    user = session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    ).scalar_one_or_none()

    if not user:
        await message.answer(
            "Open the app with /start and create your character first."
        )
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
