"""
Profile handler — LifeQuest Telegram Bot.

Provides the /profile command that displays the authenticated user's
character statistics (name, class, level, XP, coins, avatar).

Architecture:
  - Uses aiogram 3.x Router for modular handler registration.
  - Receives a pre-injected SQLAlchemy Session via DatabaseMiddleware.
  - Reads from the User model (database/users.py).
"""

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.users import User

# Module-level router — registered in main.py under dp.include_router().
router = Router()


@router.message(Command("profile"))
async def cmd_profile(
    message: types.Message,
    state: FSMContext,
    session: Session,
) -> None:
    """
    Handle the /profile command.

    Looks up the Telegram user in the database and replies with their
    current character profile. If the user hasn't registered yet they are
    prompted to open the app via /start first.

    Parameters
    ----------
    message : types.Message
        The incoming Telegram message containing the command.
    state : FSMContext
        Finite-state-machine context (unused here, required by signature).
    session : Session
        Database session provided by DatabaseMiddleware.
    """
    # Fetch the user record linked to this Telegram account.
    user = session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    ).scalar_one_or_none()

    # Guard: unregistered visitors.
    if not user:
        await message.answer(
            "Open the app with /start and create your character first."
        )
        return

    # Compose and send the profile summary.
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
