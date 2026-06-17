from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.users import User
import hashlib

router = Router()


class AuthStates(StatesGroup):
    """Authorization states"""
    waiting_for_login = State()
    waiting_for_password = State()
    waiting_for_confirm = State()


async def get_user_by_telegram_id(session: AsyncSession, telegram_id: int) -> User | None:
    """Get user by telegram ID"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_login(session: AsyncSession, login: str) -> User | None:
    """Get user by login"""
    result = await session.execute(
        select(User).where(User.username == login)
    )
    return result.scalar_one_or_none()


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, session: AsyncSession):
    """Handle /start command"""
    user = await get_user_by_telegram_id(session, message.from_user.id)
    
    if user:
        # User exists
        await message.answer(
            f"Welcome back, {message.from_user.first_name or 'Player'}! 🎮\n\n"
            "Enter /profile to view your profile"
        )
        await state.clear()
    else:
        # New user - need to register
        await message.answer(
            "Welcome to TG BOT RPG! 🎮\n\n"
            "This is a gamified self-development experience.\n"
            "Let's create your account.\n\n"
            "Choose a login:"
        )
        await state.set_state(AuthStates.waiting_for_login)


@router.message(AuthStates.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext, session: AsyncSession):
    """Process login input"""
    login = message.text.strip()
    
    # Validate login
    if len(login) < 3:
        await message.answer("Login must be at least 3 characters. Try again:")
        return
    
    if len(login) > 20:
        await message.answer("Login must be at most 20 characters. Try again:")
        return
    
    if not login.replace('_', '').replace('-', '').isalnum():
        await message.answer(
            "Login can only contain letters, numbers, hyphens, and underscores. Try again:"
        )
        return
    
    # Check if login already exists
    existing_user = await get_user_by_login(session, login)
    if existing_user:
        await message.answer(
            f"Login '{login}' is already taken. Choose another:"
        )
        return
    
    # Store login in context
    await state.update_data(login=login)
    
    await message.answer(
        f"Good! Your login: {login}\n\n"
        "Now choose a password (at least 6 characters):"
    )
    await state.set_state(AuthStates.waiting_for_password)


@router.message(AuthStates.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    """Process password input"""
    password = message.text
    
    # Validate password
    if len(password) < 6:
        await message.answer(
            "Password must be at least 6 characters. Try again:"
        )
        return
    
    # Store password in context
    await state.update_data(password=password)
    
    data = await state.get_data()
    login = data.get('login')
    
    # Show confirmation
    await message.answer(
        f"✓ Login: {login}\n"
        f"✓ Password: {'*' * len(password)}\n\n"
        "Is everything correct?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✅ Yes"), KeyboardButton(text="❌ No")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )
    await state.set_state(AuthStates.waiting_for_confirm)


@router.message(AuthStates.waiting_for_confirm)
async def process_confirm(message: types.Message, state: FSMContext, session: AsyncSession):
    """Process confirmation"""
    if message.text == "✅ Yes":
        data = await state.get_data()
        login = data.get('login')
        password = data.get('password')
        
        try:
            hashed_password = hash_password(password)
            
            # Create new user
            new_user = User(
                telegram_id=message.from_user.id,
                username=login,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            session.add(new_user)
            await session.commit()
            
            await message.answer(
                f"✅ Registration complete!\n\n"
                f"Welcome, {message.from_user.first_name or 'Player'}! 🎮",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.clear()
            
        except Exception as e:
            await message.answer(
                f"❌ Error during registration: {str(e)}\n\n"
                "Try again with /start",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.clear()
    
    elif message.text == "❌ No":
        await message.answer(
            "Let's try again. Choose a login:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(AuthStates.waiting_for_login)
    
    else:
        await message.answer("Please choose ✅ Yes or ❌ No")
