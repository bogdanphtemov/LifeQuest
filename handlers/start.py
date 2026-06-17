from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select
from sqlalchemy.orm import Session
from database.users import User
import hashlib
import hmac
import logging
import os

router = Router()
logger = logging.getLogger(__name__)


class AuthStates(StatesGroup):
    """Authorization states"""
    waiting_for_register_username = State()
    waiting_for_register_password = State()
    waiting_for_existing_password = State()
    waiting_for_login_username = State()
    waiting_for_login_password = State()


def get_user_by_telegram_id(session: Session, telegram_id: int) -> User | None:
    """Get user by telegram ID"""
    result = session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


def get_user_by_login(session: Session, login: str) -> User | None:
    """Get user by login"""
    result = session.execute(
        select(User).where(User.username == login)
    )
    return result.scalar_one_or_none()


def normalize_username(username: str) -> str:
    """Normalize username for consistent login lookup."""
    return username.strip().lower()


def validate_username(username: str) -> str | None:
    """Return an error message when username is invalid."""
    if len(username) < 3:
        return "Login must be at least 3 characters. Try again:"

    if len(username) > 20:
        return "Login must be at most 20 characters. Try again:"

    if not username.replace("_", "").replace("-", "").isalnum():
        return "Login can only contain letters, numbers, hyphens, and underscores. Try again:"

    return None


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC with a per-user salt."""
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )
    return f"{salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str | None) -> bool:
    """Verify a password against supported stored hash formats."""
    if not stored_hash:
        return False

    if "$" not in stored_hash:
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()
        return hmac.compare_digest(legacy_hash, stored_hash)

    salt_hex, hash_hex = stored_hash.split("$", 1)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        600_000,
    )
    return hmac.compare_digest(password_hash.hex(), hash_hex)


async def mark_authenticated(state: FSMContext, user: User):
    """Store the authenticated user id in FSM state data."""
    await state.clear()
    await state.update_data(authenticated_user_id=user.id)


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: Session):
    """Handle /start command"""
    user = get_user_by_telegram_id(session, message.from_user.id)
    
    if user:
        await message.answer(
            f"Welcome back, {user.display_name or user.username}!\n\n"
            "Enter your password to log in:"
        )
        await state.set_state(AuthStates.waiting_for_existing_password)
        return

    await message.answer(
        "Welcome to TG BOT RPG!\n\n"
        "This is a gamified self-development experience.\n"
        "Let's create your account.\n\n"
        "Choose a login:"
    )
    await state.set_state(AuthStates.waiting_for_register_username)


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext, session: Session):
    """Start login flow."""
    user = get_user_by_telegram_id(session, message.from_user.id)
    
    if user:
        await message.answer("Enter your password:")
        await state.set_state(AuthStates.waiting_for_existing_password)
        return

    await message.answer("Enter your login:")
    await state.set_state(AuthStates.waiting_for_login_username)


@router.message(AuthStates.waiting_for_existing_password)
async def process_existing_password(
    message: types.Message,
    state: FSMContext,
    session: Session,
):
    """Authorize an existing Telegram-linked user."""
    user = get_user_by_telegram_id(session, message.from_user.id)
    if not user:
        await message.answer("Account was not found. Use /start to register.")
        await state.clear()
        return

    if not verify_password(message.text or "", user.password_hash):
        await message.answer("Wrong password. Try again or use /start.")
        return

    await mark_authenticated(state, user)
    await message.answer(
        f"Logged in as {user.display_name or user.username}.\n\n"
        "Use /profile to view your character."
    )


@router.message(AuthStates.waiting_for_login_username)
async def process_login_username(message: types.Message, state: FSMContext, session: Session):
    """Process login username for unlinked Telegram accounts."""
    login = normalize_username(message.text or "")
    user = get_user_by_login(session, login)
    
    if not user:
        await message.answer("Login was not found. Try again or use /start to register:")
        return

    await state.update_data(login=login)
    await message.answer("Enter your password:")
    await state.set_state(AuthStates.waiting_for_login_password)


@router.message(AuthStates.waiting_for_login_password)
async def process_login_password(message: types.Message, state: FSMContext, session: Session):
    """Authorize by username and password."""
    data = await state.get_data()
    user = get_user_by_login(session, data.get("login", ""))

    if not user or not verify_password(message.text or "", user.password_hash):
        await message.answer("Wrong login or password. Try /login again.")
        await state.clear()
        return

    if user.telegram_id and user.telegram_id != message.from_user.id:
        await message.answer("This account is already linked to another Telegram user.")
        await state.clear()
        return

    if user.telegram_id != message.from_user.id:
        user.telegram_id = message.from_user.id
        session.commit()

    await mark_authenticated(state, user)
    await message.answer(
        f"Logged in as {user.display_name or user.username}.\n\n"
        "Use /profile to view your character."
    )


@router.message(AuthStates.waiting_for_register_username)
async def process_register_username(message: types.Message, state: FSMContext, session: Session):
    """Process registration username input."""
    login = normalize_username(message.text or "")
    validation_error = validate_username(login)
    if validation_error:
        await message.answer(validation_error)
        return

    existing_user = get_user_by_login(session, login)
    if existing_user:
        await message.answer(
            f"Login '{login}' is already taken. Choose another or use /login:"
        )
        return

    await state.update_data(login=login)
    await message.answer(
        f"Good! Your login: {login}\n\n"
        "Now choose a password (at least 6 characters):"
    )
    await state.set_state(AuthStates.waiting_for_register_password)


@router.message(AuthStates.waiting_for_register_password)
async def process_register_password(message: types.Message, state: FSMContext, session: Session):
    """Create a new user account."""
    password = message.text or ""
    
    if len(password) < 6:
        await message.answer(
            "Password must be at least 6 characters. Try again:"
        )
        return
    data = await state.get_data()
    login = data.get("login")

    try:
        new_user = User(
            telegram_id=message.from_user.id,
            username=login,
            password_hash=hash_password(password),
            display_name=message.from_user.first_name or login,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            avatar="pixel_adventurer",
            character_class="adventurer",
            level=1,
            experience=0,
            coins=0,
        )
        session.add(new_user)
        session.commit()

        await mark_authenticated(state, new_user)
        await message.answer(
            "Registration complete!\n\n"
            f"Welcome, {new_user.display_name or new_user.username}.\n"
            "Use /profile to view your character."
        )
    except Exception:
        logger.exception("Error during user registration")
        await message.answer(
            "Error during registration.\n\n"
            "Try again with /start"
        )
        await state.clear()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Show basic bot commands."""
    await message.answer(
        "Commands:\n"
        "/start - register or log in\n"
        "/login - log in to an existing account\n"
        "/profile - show your RPG profile"
    )
