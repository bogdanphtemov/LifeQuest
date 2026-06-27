"""
Telegram bot command and callback handlers for authentication and onboarding.

This module defines all handlers related to user registration, login (via
username/password), account deletion, and the main /start command that opens
the LifeQuest Mini App. It uses aiogram's FSM (Finite State Machine) to manage
multi-step conversational flows, and SQLAlchemy sessions (injected by the
DatabaseMiddleware from main.py) for all database operations.

Module-level dependencies:
- router (aiogram.Router): Registered in main.py with dp.include_router().
- AuthStates (StatesGroup): Defines all FSM states used across these flows.
- Each handler receives a `session: Session` kwarg via middleware injection.
"""

from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from config import WEB_APP_URL
from database.users import User
import hashlib
import hmac
import logging
import os
import time
from collections import defaultdict
from urllib.parse import urlparse

router = Router()
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory rate limiting (sliding window per Telegram user ID)
# ---------------------------------------------------------------------------

_login_attempts: dict[int, list[float]] = defaultdict(list)
"""Track timestamps of failed login attempts per user_id."""

MAX_LOGIN_ATTEMPTS = 5
"""Max consecutive failed login attempts before lockout."""

LOGIN_WINDOW_SECONDS = 300  # 5 хвилин
"""Time window for counting login attempts."""


def _is_login_rate_limited(user_id: int) -> bool:
    """
    Check if the user exceeded the login attempt limit.

    Removes expired attempts (older than LOGIN_WINDOW_SECONDS),
    then checks if the count is still at or above MAX_LOGIN_ATTEMPTS.
    """
    now = time.time()
    attempts = _login_attempts[user_id]
    # Keep only attempts within the window
    _login_attempts[user_id] = [t for t in attempts if now - t < LOGIN_WINDOW_SECONDS]
    if len(_login_attempts[user_id]) >= MAX_LOGIN_ATTEMPTS:
        return True
    _login_attempts[user_id].append(now)
    return False


def _reset_login_attempts(user_id: int) -> None:
    """Clear the attempt counter on successful login."""
    _login_attempts.pop(user_id, None)


# ---------------------------------------------------------------------------
# Registration rate limit (separate counter for a different threshold)
# ---------------------------------------------------------------------------

_register_attempts: dict[int, list[float]] = defaultdict(list)
MAX_REGISTER_ATTEMPTS = 3
REGISTER_WINDOW_SECONDS = 3600  # 1 година


def _is_register_rate_limited(user_id: int) -> bool:
    """Check if the user exceeded the registration attempt limit."""
    now = time.time()
    attempts = _register_attempts[user_id]
    _register_attempts[user_id] = [t for t in attempts if now - t < REGISTER_WINDOW_SECONDS]
    if len(_register_attempts[user_id]) >= MAX_REGISTER_ATTEMPTS:
        return True
    _register_attempts[user_id].append(now)
    return False


class AuthStates(StatesGroup):
    """
    FSM states for multi-step authentication and account deletion flows.

    Each state corresponds to a step where the bot waits for user text input.
    The flow transitions between states via @router.message(state) handlers.
    """
    waiting_for_register_username = State()
    waiting_for_register_password = State()
    waiting_for_existing_password = State()
    waiting_for_login_username = State()
    waiting_for_login_password = State()
    waiting_for_delete_username = State()
    waiting_for_delete_password = State()


def get_user_by_telegram_id(session: Session, telegram_id: int) -> User | None:
    """
    Look up a user by their Telegram user ID.

    Used to detect whether an existing Telegram user is already registered.
    """
    result = session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


def get_user_by_login(session: Session, login: str) -> User | None:
    """
    Look up a user by their normalized username (case-insensitive, trimmed).

    Supports both bare usernames and "@username" format by including both in
    the lookup set.
    """
    normalized_login = normalize_username(login)
    username_column = func.lower(func.trim(User.username))
    result = session.execute(
        select(User).where(
            username_column.in_((normalized_login, f"@{normalized_login}"))
        )
    )
    return result.scalar_one_or_none()


def normalize_username(username: str) -> str:
    """Normalize a username for consistent lookup: strip whitespace,
    remove leading '@', and convert to lowercase."""
    return username.strip().lstrip("@").lower()


def validate_username(username: str) -> str | None:
    """
    Validate a proposed username and return an error message if invalid.

    Rules:
    - Must be between 3 and 20 characters.
    - May only contain letters, digits, hyphens, and underscores.
    """
    if len(username) < 3:
        return "Login must be at least 3 characters. Try again:"

    if len(username) > 20:
        return "Login must be at most 20 characters. Try again:"

    if not username.replace("_", "").replace("-", "").isalnum():
        return "Login can only contain letters, numbers, hyphens, and underscores. Try again:"

    return None


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a random 16-byte salt.

    Output format: "<salt_hex>$<hash_hex>" — stored in User.password_hash.
    Uses 600 000 iterations for reasonable brute-force resistance.
    """
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )
    return f"{salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_hash: str | None) -> bool:
    """
    Verify a password against its stored hash.

    Supports two formats:
    - New format: "<salt_hex>$<hash_hex>" (PBKDF2-HMAC-SHA256).
    - Legacy format: plain SHA256 hex string (used before migration).
    Returns False for None, empty strings, or "telegram$..." placeholders.
    """
    if not stored_hash:
        return False

    if "$" not in stored_hash:
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()
        return hmac.compare_digest(legacy_hash, stored_hash)

    salt_hex, hash_hex = stored_hash.split("$", 1)
    if salt_hex == "telegram":
        return False

    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )
    return hmac.compare_digest(password_hash.hex(), hash_hex)


async def mark_authenticated(state: FSMContext, user: User):
    """
    Persist a successful authentication in the FSM state.

    Clears any previous state data, then stores the authenticated user's
    primary key so other handlers (e.g. /profile) can identify the user.
    """
    await state.clear()
    await state.update_data(authenticated_user_id=user.id)


def is_valid_web_app_url(url: str) -> bool:
    """
    Validate that a URL is suitable for use as a Telegram Mini App button.

    Telegram requires Mini App buttons to point to a public HTTPS endpoint
    without spaces or '->' (which appear in ngrok forwarding strings).
    """
    parsed_url = urlparse(url)
    return (
        parsed_url.scheme == "https"
        and bool(parsed_url.netloc)
        and " " not in url
        and "->" not in url
    )


def build_start_keyboard() -> InlineKeyboardMarkup:
    """
    Build the inline keyboard for the /start command.

    Includes:
    - "Open LifeQuest" button that launches the Telegram Mini App (if configured).
    - "Delete account" button that triggers the deletion flow via callback.
    """
    buttons = []

    if is_valid_web_app_url(WEB_APP_URL):
        buttons.append([
            InlineKeyboardButton(
                text="Open LifeQuest",
                web_app=WebAppInfo(url=WEB_APP_URL),
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="Delete account",
            callback_data="delete_account",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def start_delete_account_flow(message: types.Message, state: FSMContext):
    """
    Shared entry point for account deletion, used by both /delete_account
    command and the "Delete account" inline button callback.

    Clears state and prompts for the account login.
    """
    await state.clear()
    await message.answer(
        "Account deletion started.\n\n"
        "Enter the login of the account you want to delete:"
    )
    await state.set_state(AuthStates.waiting_for_delete_username)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: Session):
    """
    Handle the /start command — the main entry point for new and returning users.

    Clears any ongoing FSM conversation and presents the Mini App launch button.
    If WEB_APP_URL is not a valid HTTPS URL, shows a configuration hint instead.
    """
    await state.clear()

    if is_valid_web_app_url(WEB_APP_URL):
        await message.answer(
            "Welcome to TG BOT RPG!\n\n"
            "Open the RPG app to create your character, manage quests, and track your progress.",
            reply_markup=build_start_keyboard(),
        )
        return

    await message.answer(
        "Welcome to TG BOT RPG!\n\n"
        "The Mini App URL is not ready for Telegram yet:\n"
        f"{WEB_APP_URL}\n\n"
        "Telegram Mini App buttons require a public HTTPS WEB_APP_URL. "
        "Put only the HTTPS URL in .env, without the arrow or local address. "
        "Example: WEB_APP_URL=https://example.ngrok-free.app",
        reply_markup=build_start_keyboard(),
    )


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext, session: Session):
    """
    Handle the /login command — start the legacy username/password login flow.

    Two scenarios:
    - User already has a Telegram-linked account: ask for password directly.
    - User is not yet linked: ask for a login first.
    """
    user = get_user_by_telegram_id(session, message.from_user.id)
    
    if user:
        await message.answer("Enter your password:")
        await state.set_state(AuthStates.waiting_for_existing_password)
        return

    await message.answer("Enter your login:")
    await state.set_state(AuthStates.waiting_for_login_username)


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Handle the /cancel command — abort any ongoing multi-step flow.

    Clears the FSM state and resets the conversation back to the idle state.
    """
    await state.clear()
    await message.answer("Current action cancelled.")


@router.message(Command("delete_account"))
async def cmd_delete_account(message: types.Message, state: FSMContext):
    """Handle the /delete_account command — start account deletion flow."""
    await start_delete_account_flow(message, state)


@router.callback_query(lambda callback: callback.data == "delete_account")
async def callback_delete_account(callback: types.CallbackQuery, state: FSMContext):
    """
    Handle the "Delete account" inline button press.

    Routes to the same deletion flow as the /delete_account command.
    """
    await callback.answer()
    if callback.message:
        await start_delete_account_flow(callback.message, state)


# ---------------------------------------------------------------------------
# FSM step handlers — Login flow
# ---------------------------------------------------------------------------


@router.message(AuthStates.waiting_for_existing_password)
async def process_existing_password(
    message: types.Message,
    state: FSMContext,
    session: Session,
):
    """
    FSM step: verify password for a user who already has a Telegram-linked account.

    Entered from /login when the user's Telegram ID is already in the database.
    On success, calls mark_authenticated() and confirms login.
    On failure, stays in this state to allow retry.
    """
    user_id = message.from_user.id

    # ---- Rate limit check ----
    if _is_login_rate_limited(user_id):
        await message.answer(
            "⛔ Too many login attempts. Please wait 5 minutes and try again."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded login attempts")
        return
    # --------------------------

    user = get_user_by_telegram_id(session, user_id)
    if not user:
        await message.answer("Account was not found. Use /start to register.")
        await state.clear()
        return

    if not verify_password(message.text or "", user.password_hash):
        await message.answer("Wrong password. Try again or use /start.")
        return

    # Successful login — reset counter
    _reset_login_attempts(user_id)

    await mark_authenticated(state, user)
    await message.answer(
        f"Logged in as {user.display_name or user.username}.\n\n"
        "Use /profile to view your character."
    )


@router.message(AuthStates.waiting_for_login_username)
async def process_login_username(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step: collect the username for a non-linked Telegram user.

    Validates that the username exists in the database.
    On success, transitions to waiting_for_login_password.
    """
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
    """
    FSM step: verify password and complete the login for a non-linked user.

    On success, links the Telegram ID to the account (if not already linked
    to another user) and calls mark_authenticated().
    """
    user_id = message.from_user.id

    # ---- Rate limit check ----
    if _is_login_rate_limited(user_id):
        await message.answer(
            "⛔ Too many login attempts. Please wait 5 minutes and try again."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded login attempts")
        return
    # --------------------------

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

    # Successful login — reset counter
    _reset_login_attempts(user_id)

    await mark_authenticated(state, user)
    await message.answer(
        f"Logged in as {user.display_name or user.username}.\n\n"
        "Use /profile to view your character."
    )


# ---------------------------------------------------------------------------
# FSM step handlers — Account deletion flow
# ---------------------------------------------------------------------------


@router.message(AuthStates.waiting_for_delete_username)
async def process_delete_username(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step: collect the username for account deletion.

    Validates that the account exists and is not linked to another Telegram user.
    On success, transitions to waiting_for_delete_password.
    """
    login = normalize_username(message.text or "")
    user = get_user_by_login(session, login)

    if not user:
        await message.answer("Login was not found. Try again or use /cancel.")
        return

    if user.telegram_id and user.telegram_id != message.from_user.id:
        await message.answer(
            "This account is linked to another Telegram user. Deletion cancelled."
        )
        await state.clear()
        return

    await state.update_data(delete_login=login)
    await message.answer(
        "Enter the password for this account to confirm deletion:"
    )
    await state.set_state(AuthStates.waiting_for_delete_password)


@router.message(AuthStates.waiting_for_delete_password)
async def process_delete_password(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step: verify password and permanently delete the user account.

    Performs a final verification, then deletes the User row from the database.
    On any error, rolls back the transaction and notifies the user.
    """
    user_id = message.from_user.id

    # ---- Rate limit check (also protect deletion) ----
    if _is_login_rate_limited(user_id):
        await message.answer(
            "⛔ Too many attempts. Please wait 5 minutes and try again."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded delete attempts")
        return
    # --------------------------------------------------

    data = await state.get_data()
    login = data.get("delete_login", "")
    user = get_user_by_login(session, login)

    if not user or not verify_password(message.text or "", user.password_hash):
        await message.answer("Wrong login or password. Deletion cancelled.")
        await state.clear()
        return

    if user.telegram_id and user.telegram_id != message.from_user.id:
        await message.answer(
            "This account is linked to another Telegram user. Deletion cancelled."
        )
        await state.clear()
        return

    deleted_login = user.username

    try:
        session.delete(user)
        session.commit()
    except Exception:
        logger.exception("Error during account deletion")
        session.rollback()
        await message.answer("Error during account deletion. Try again later.")
        await state.clear()
        return

    _reset_login_attempts(user_id)
    await state.clear()
    await message.answer(
        f"Account '{deleted_login}' was deleted successfully."
    )


# ---------------------------------------------------------------------------
# FSM step handlers — Registration flow (if triggered by external /start logic)
# ---------------------------------------------------------------------------


@router.message(AuthStates.waiting_for_register_username)
async def process_register_username(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step: collect and validate a new username during registration.

    Checks uniqueness and format rules. On success, transitions to password input.
    """
    user_id = message.from_user.id

    # ---- Rate limit check for registration ----
    if _is_register_rate_limited(user_id):
        await message.answer(
            "⛔ You have reached the maximum number of registration attempts "
            "for today. Please try again later."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded register attempts")
        return
    # -------------------------------------------

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
    """
    FSM step: finalise user registration with password and create the database record.

    Creates a new User row with the Telegram ID, hashed password, and default
    RPG attributes. On completion, calls mark_authenticated() so the user is
    immediately logged in.
    """
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


# ---------------------------------------------------------------------------
# Utility command
# ---------------------------------------------------------------------------


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle the /help command — list all available bot commands."""
    await message.answer(
        "Commands:\n"
        "/start - open the LifeQuest Mini App\n"
        "/login - legacy chat login\n"
        "/profile - show your RPG profile\n"
        "/delete_account - delete an account by login and password\n"
        "/cancel - cancel the current action"
    )
