"""
Telegram bot command and callback handlers for registration and account deletion.

This module defines all handlers related to user registration (via Telegram bot in
text format), automatic login via telegram_id, account deletion, and the main /start
command that opens the LifeQuest Mini App.

Key changes:
- Registration is handled entirely in the Telegram bot (text format, no frontend form)
- Login is automatic via telegram_id (unique identifier)
- Account deletion uses telegram_id (auto-detected) + password confirmation
- Frontend / Mini App just pulls data from the database and shows the game screen

Module-level dependencies:
- router (aiogram.Router): Registered in main.py with dp.include_router().
- RegisterStates (StatesGroup): FSM states for bot-based registration flow.
- DeleteStates (StatesGroup): FSM states for account deletion flow.
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
"""Track timestamps of failed attempts per user_id."""

MAX_LOGIN_ATTEMPTS = 5
"""Max consecutive failed attempts before lockout."""

LOGIN_WINDOW_SECONDS = 300  # 5 minutes
"""Time window for counting attempts."""


def _is_login_rate_limited(user_id: int) -> bool:
    """
    Check if the user exceeded the login attempt limit.

    Removes expired attempts (older than LOGIN_WINDOW_SECONDS),
    then checks if the count is still at or above MAX_LOGIN_ATTEMPTS.
    """
    now = time.time()
    attempts = _login_attempts[user_id]
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
REGISTER_WINDOW_SECONDS = 3600  # 1 hour


# ---------------------------------------------------------------------------
# FSM States for Registration and Deletion flows
# ---------------------------------------------------------------------------


class RegisterStates(StatesGroup):
    """
    FSM states for the bot-based registration flow.

    The user is guided through 4 steps:
    1. Enter username (3-20 chars, unique)
    2. Enter display name (optional)
    3. Choose character class (via inline keyboard)
    4. Set password (for account deletion confirmation)
    """
    waiting_for_username = State()
    waiting_for_display_name = State()
    waiting_for_character_class = State()
    waiting_for_password = State()


class DeleteStates(StatesGroup):
    """
    FSM states for account deletion flow.

    Since telegram_id is auto-detected, only password confirmation is needed.
    """
    waiting_for_password = State()


def _is_register_rate_limited(user_id: int) -> bool:
    """Check if the user exceeded the registration attempt limit."""
    now = time.time()
    attempts = _register_attempts[user_id]
    _register_attempts[user_id] = [t for t in attempts if now - t < REGISTER_WINDOW_SECONDS]
    if len(_register_attempts[user_id]) >= MAX_REGISTER_ATTEMPTS:
        return True
    _register_attempts[user_id].append(now)
    return False


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


def build_start_keyboard(is_registered: bool = False) -> InlineKeyboardMarkup:
    """
    Build the inline keyboard for the /start command.

    Args:
        is_registered: Whether the user is already registered.
                       If True, shows "Open LifeQuest", "Profile", and
                       "Delete account" buttons.
                       If False, registration flow is in progress.

    Includes:
    - "Open LifeQuest" button that launches the Telegram Mini App (if configured).
    - "Profile" button (only for registered users).
    - "Delete account" button (only for registered users).
    """
    buttons = []

    if is_valid_web_app_url(WEB_APP_URL):
        buttons.append([
            InlineKeyboardButton(
                text="🎮 Open LifeQuest",
                web_app=WebAppInfo(url=WEB_APP_URL),
            )
        ])

    if is_registered:
        buttons.append([
            InlineKeyboardButton(
                text="👤 Profile",
                callback_data="show_profile",
            ),
            InlineKeyboardButton(
                text="🗑️ Delete account",
                callback_data="delete_account",
            ),
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def start_registration(message: types.Message, state: FSMContext):
    """Start the registration flow for a new user."""
    await state.clear()
    await message.answer(
        "🌟 Welcome to **LifeQuest**!\n\n"
        "You are a new adventurer in this world. Let's create your character!\n\n"
        "**Step 1 of 4:**\n"
        "Enter your **username** (in-game login):\n"
        "• 3 to 20 characters\n"
        "• Only letters, numbers, hyphens (-) and underscores (_)\n"
        "• Must be unique"
    )
    await state.set_state(RegisterStates.waiting_for_username)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: Session):
    """
    Handle the /start command — the main entry point for new and returning players.

    Logic:
    1. Clear any previous FSM state
    2. Look up the user in the database by telegram_id
    3. If USER EXISTS:
       - Show "Welcome back!" + buttons (Mini App, Profile, Delete)
    4. If USER NOT FOUND:
       - Start the registration flow (start_registration)
    """
    await state.clear()

    user = get_user_by_telegram_id(session, message.from_user.id)

    if user:
        # User exists — show main menu
        class_emojis = {
            "adventurer": "⚔️",
            "warrior": "🛡️",
            "mage": "🔮",
            "ranger": "🏹",
        }
        class_emoji = class_emojis.get(user.character_class, "⚔️")

        welcome_text = (
            f"🎮 **Welcome back, {user.display_name or user.username}!**\n\n"
            f"{class_emoji} Class: {user.character_class.capitalize()}\n"
            f"🎚️ Level: {user.level}\n"
            f"⭐ Experience: {user.experience}\n"
            f"🪙 Coins: {user.coins}\n\n"
            "Click the button below to enter the game! 🎮"
        )

        await message.answer(
            welcome_text,
            reply_markup=build_start_keyboard(is_registered=True),
        )
    else:
        # User not found — start registration
        await start_registration(message, state)


@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    """
    Handle the /cancel command — abort any ongoing multi-step flow.

    Clears the FSM state and resets the conversation back to the idle state.
    """
    await state.clear()
    await message.answer("❌ Current action cancelled.")


@router.message(Command("delete_account"))
async def cmd_delete_account(message: types.Message, state: FSMContext, session: Session):
    """Handle the /delete_account command — start account deletion flow.

    Since telegram_id is auto-detected, only password confirmation is needed.
    """
    user = get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer(
            "ℹ️ You don't have an account yet. "
            "Use /start to create a character!"
        )
        return

    await state.clear()
    await state.update_data(delete_user_id=user.id)
    await message.answer(
        f"🗑️ **Account Deletion**\n\n"
        f"Do you want to delete account **{user.username}**?\n"
        f"⚠️ This will **permanently** delete your character and all progress!\n\n"
        "Enter your **password** to confirm:",
    )
    await state.set_state(DeleteStates.waiting_for_password)


@router.callback_query(lambda callback: callback.data == "delete_account")
async def callback_delete_account(callback: types.CallbackQuery, state: FSMContext, session: Session):
    """
    Handle the "Delete account" inline button press.

    Routes to the same deletion flow as the /delete_account command.
    """
    await callback.answer()
    if callback.message:
        user = get_user_by_telegram_id(session, callback.from_user.id)
        if not user:
            await callback.message.answer(
                "ℹ️ You don't have an account yet. "
                "Use /start to create a character!"
            )
            return

        await state.clear()
        await state.update_data(delete_user_id=user.id)
        await callback.message.answer(
            f"🗑️ **Account Deletion**\n\n"
            f"Do you want to delete account **{user.username}**?\n"
            f"⚠️ This will **permanently** delete your character and all progress!\n\n"
            "Enter your **password** to confirm:",
        )
        await state.set_state(DeleteStates.waiting_for_password)


# ---------------------------------------------------------------------------
# FSM step handlers — Registration flow (in bot, text format)
# ---------------------------------------------------------------------------


@router.message(RegisterStates.waiting_for_username)
async def process_register_username(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step 1/4: collect and validate username during registration.

    Checks format rules (3-20 chars, alphanumeric + - _) and uniqueness.
    On success, transitions to display name input.
    """
    user_id = message.from_user.id

    # ---- Rate limit check for registration ----
    if _is_register_rate_limited(user_id):
        await message.answer(
            "⛔ You have reached the maximum number of registration attempts. "
            "Please try again later."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded register attempts")
        return

    login = normalize_username(message.text or "")
    validation_error = validate_username(login)
    if validation_error:
        await message.answer(validation_error)
        return

    existing_user = get_user_by_login(session, login)
    if existing_user:
        await message.answer(
            f"❌ Login '{login}' is already taken. Choose another:"
        )
        return

    first_name = message.from_user.first_name or login
    await state.update_data(username=login)
    await message.answer(
        f"✅ Great! Your username: **{login}**\n\n"
        "**Step 2 of 4:**\n"
        "Enter your **hero name** (what you'll be called in the world of LifeQuest):\n"
        f"• Or send /skip to use '{first_name}'"
    )
    await state.set_state(RegisterStates.waiting_for_display_name)


@router.message(RegisterStates.waiting_for_display_name, Command("skip"))
async def process_skip_display_name(message: types.Message, state: FSMContext):
    """
    FSM step 2/4 (skip): skip display name and use Telegram first name.
    """
    display_name = message.from_user.first_name or message.from_user.username or "Adventurer"
    await state.update_data(display_name=display_name)
    await ask_character_class(message, state)


@router.message(RegisterStates.waiting_for_display_name)
async def process_display_name(message: types.Message, state: FSMContext):
    """
    FSM step 2/4: collect display name for the character.
    """
    display_name = (message.text or "").strip()

    if not display_name:
        await message.answer("Hero name cannot be empty. Try again or /skip:")
        return

    if len(display_name) > 50:
        await message.answer("Hero name is too long (max 50 characters). Try again:")
        return

    await state.update_data(display_name=display_name)
    await ask_character_class(message, state)


async def ask_character_class(message: types.Message, state: FSMContext):
    """Ask the user to choose a character class via inline keyboard."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚔️ Adventurer", callback_data="class_adventurer"),
            InlineKeyboardButton(text="🛡️ Warrior", callback_data="class_warrior"),
        ],
        [
            InlineKeyboardButton(text="🔮 Mage", callback_data="class_mage"),
            InlineKeyboardButton(text="🏹 Ranger", callback_data="class_ranger"),
        ],
    ])
    await message.answer(
        "**Step 3 of 4:**\n"
        "Choose your **character class**:",
        reply_markup=keyboard,
    )
    await state.set_state(RegisterStates.waiting_for_character_class)


@router.callback_query(lambda c: c.data and c.data.startswith("class_"))
async def process_character_class(callback: types.CallbackQuery, state: FSMContext):
    """
    FSM step 3/4: process the chosen character class via callback.
    """
    class_map = {
        "class_adventurer": ("adventurer", "Adventurer"),
        "class_warrior": ("warrior", "Warrior"),
        "class_mage": ("mage", "Mage"),
        "class_ranger": ("ranger", "Ranger"),
    }

    class_key = callback.data
    if class_key not in class_map:
        await callback.answer("Unknown class. Try again.")
        return

    class_value, class_label = class_map[class_key]
    await state.update_data(character_class=class_value)

    await callback.answer()
    await callback.message.edit_text(
        f"✅ Selected class: **{class_label}**\n\n"
        "**Step 4 of 4 (final):**\n"
        "Enter a **password** for your account:\n"
        "• At least 6 characters\n"
        "• You'll need it to confirm account deletion"
    )
    await state.set_state(RegisterStates.waiting_for_password)


@router.message(RegisterStates.waiting_for_password)
async def process_register_password(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step 4/4: finalise user registration with password and create the database record.

    Creates a new User row with the Telegram ID, hashed password, and all collected
    RPG attributes. On completion, shows success message with "Open LifeQuest" button.
    """
    password = message.text or ""

    if len(password) < 6:
        await message.answer(
            "❌ Password must be at least 6 characters. Try again:"
        )
        return

    data = await state.get_data()
    username = data.get("username")
    display_name = data.get("display_name", message.from_user.first_name or username)
    character_class = data.get("character_class", "adventurer")

    try:
        new_user = User(
            telegram_id=message.from_user.id,
            username=username,
            password_hash=hash_password(password),
            display_name=display_name,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            avatar="pixel_adventurer",
            character_class=character_class,
            level=1,
            experience=0,
            coins=0,
        )
        session.add(new_user)
        session.commit()

        await state.clear()
        await message.answer(
            f"🎉 **Congratulations, {display_name}!**\n\n"
            f"Your character has been created successfully!\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"📛 Name: {display_name}\n"
            f"🔑 Login: {username}\n"
            f"⚔️ Class: {character_class.capitalize()}\n"
            f"🎚️ Level: 1\n"
            f"━━━━━━━━━━━━━━━━━\n\n"
            "Click the button below to enter the game! 🎮",
            reply_markup=build_start_keyboard(is_registered=True),
        )
    except Exception as e:
        logger.exception("Error during user registration")
        session.rollback()
        await message.answer(
            "❌ Error during registration. Try again with /start"
        )
        await state.clear()


# ---------------------------------------------------------------------------
# FSM step handlers — Account deletion flow (telegram_id + password)
# ---------------------------------------------------------------------------


@router.message(DeleteStates.waiting_for_password)
async def process_delete_password(message: types.Message, state: FSMContext, session: Session):
    """
    FSM step: verify password and permanently delete the user account.

    Uses telegram_id (auto-detected) + password confirmation.
    On success, performs COMPLETE DATA CLEANUP of the user account.

    Data cleanup logic:
    1. Delete the user from the users table
    2. (Future) Delete related data:
       - quest progress
       - inventory / items
       - achievements
       - message history
       - settings
    """
    user_id = message.from_user.id

    # ---- Rate limit check ----
    if _is_login_rate_limited(user_id):
        await message.answer(
            "⛔ Too many attempts. Please wait 5 minutes and try again."
        )
        logger.warning(f"Rate limit hit: user {user_id} exceeded delete attempts")
        return

    data = await state.get_data()
    user = session.get(User, data.get("delete_user_id"))

    if not user or not verify_password(message.text or "", user.password_hash):
        await message.answer("❌ Wrong password. Deletion cancelled.")
        await state.clear()
        return

    # Store data for the final message
    deleted_username = user.username
    deleted_display_name = user.display_name
    deleted_telegram_id = user.telegram_id

    try:
        # ===== COMPLETE DATA CLEANUP =====

        # --- Step 1: Delete related data (future tables) ---
        # Currently no other tables exist, but the structure is ready for extension:
        #
        # session.query(QuestProgress).filter(
        #     QuestProgress.user_id == user.id
        # ).delete(synchronize_session=False)
        #
        # session.query(Inventory).filter(
        #     Inventory.user_id == user.id
        # ).delete(synchronize_session=False)
        #
        # session.query(Achievement).filter(
        #     Achievement.user_id == user.id
        # ).delete(synchronize_session=False)
        #
        # session.query(Notification).filter(
        #     Notification.user_id == user.id
        # ).delete(synchronize_session=False)
        #
        # session.query(UserSettings).filter(
        #     UserSettings.user_id == user.id
        # ).delete(synchronize_session=False)

        # --- Step 2: Delete the user ---
        session.delete(user)
        session.commit()

        logger.info(
            f"Account deleted: user_id={user.id}, "
            f"username={deleted_username}, "
            f"telegram_id={deleted_telegram_id}"
        )

    except Exception:
        logger.exception("Error during account deletion")
        session.rollback()
        await message.answer(
            "❌ Error during account deletion. Try again later."
        )
        await state.clear()
        return

    _reset_login_attempts(user_id)
    await state.clear()

    await message.answer(
        f"✅ **Account '{deleted_username}' successfully deleted.**\n\n"
        f"📝 Cleanup summary:\n"
        f"• Character '{deleted_display_name or deleted_username}' — deleted\n"
        f"• Progress — cleared\n"
        f"• Account data — completely removed\n\n"
        "Sorry to see you go... But the door is always open! 🚪\n"
        "Use /start to create a new character."
    )


# ---------------------------------------------------------------------------
# Callback: Show profile
# ---------------------------------------------------------------------------


@router.callback_query(lambda callback: callback.data == "show_profile")
async def callback_show_profile(callback: types.CallbackQuery, session: Session):
    """Handle the "Profile" inline button — show quick character summary."""
    await callback.answer()

    user = get_user_by_telegram_id(session, callback.from_user.id)
    if not user:
        if callback.message:
            await callback.message.answer(
                "ℹ️ You don't have an account yet. Use /start to create a character!"
            )
        return

    class_emojis = {
        "adventurer": "⚔️",
        "warrior": "🛡️",
        "mage": "🔮",
        "ranger": "🏹",
    }
    class_emoji = class_emojis.get(user.character_class, "⚔️")

    profile_text = (
        f"👤 **Profile: {user.display_name or user.username}**\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"📛 Name: {user.display_name or '—'}\n"
        f"🔑 Login: {user.username}\n"
        f"{class_emoji} Class: {user.character_class.capitalize()}\n"
        f"🎚️ Level: {user.level}\n"
        f"⭐ Experience: {user.experience}\n"
        f"🪙 Coins: {user.coins}\n"
        f"━━━━━━━━━━━━━━━━━"
    )

    if callback.message:
        await callback.message.answer(profile_text)


# ---------------------------------------------------------------------------
# Utility command
# ---------------------------------------------------------------------------


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Handle the /help command — list all available bot commands."""
    await message.answer(
        "📋 **Available commands:**\n\n"
        "/start - start the game / create a character\n"
        "/profile - show your character profile\n"
        "/delete_account - delete your account\n"
        "/cancel - cancel the current action\n"
        "/help - show this message"
    )
