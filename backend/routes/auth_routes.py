"""
Authentication API routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib
import asyncio
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def async_route(f):
    """Decorator to handle async route handlers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.close()
    return decorated_function


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


async def get_session():
    """Get database session from Flask app context"""
    from flask import current_app
    if current_app.async_session is None:
        raise RuntimeError("Database not initialized")
    
    async with current_app.async_session() as session:
        return session


@bp.route('/register', methods=['POST'])
@async_route
async def register():
    """Register new user
    
    Expected JSON:
    {
        "username": "username",
        "password": "password",
        "telegram_id": 123456789,
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    from database.users import User
    from flask import current_app
    
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    # Validate required fields
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    telegram_id = data.get('telegram_id')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    # Validation
    if not username or len(username) < 3 or len(username) > 20:
        return jsonify({
            'status': 'error',
            'message': 'Username must be 3-20 characters'
        }), 400
    
    if not password or len(password) < 6:
        return jsonify({
            'status': 'error',
            'message': 'Password must be at least 6 characters'
        }), 400
    
    if not telegram_id:
        return jsonify({
            'status': 'error',
            'message': 'Telegram ID is required'
        }), 400
    
    try:
        async with current_app.async_session() as session:
            # Check if user already exists
            result = await session.execute(
                select(User).where(User.username == username)
            )
            if result.scalar_one_or_none():
                return jsonify({
                    'status': 'error',
                    'message': 'Username already exists'
                }), 409
            
            # Check if telegram_id already exists
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            if result.scalar_one_or_none():
                return jsonify({
                    'status': 'error',
                    'message': 'Telegram ID already registered'
                }), 409
            
            # Create new user
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            
            return jsonify({
                'status': 'success',
                'message': 'User registered successfully',
                'user': {
                    'id': new_user.id,
                    'telegram_id': new_user.telegram_id,
                    'username': new_user.username,
                    'first_name': new_user.first_name
                }
            }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Registration failed: {str(e)}'
        }), 500


@bp.route('/login', methods=['POST'])
@async_route
async def login():
    """Login user
    
    Expected JSON:
    {
        "username": "username",
        "telegram_id": 123456789
    }
    """
    from database.users import User
    from flask import current_app
    
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    username = data.get('username', '').strip()
    telegram_id = data.get('telegram_id')
    
    if not username or not telegram_id:
        return jsonify({
            'status': 'error',
            'message': 'Username and Telegram ID are required'
        }), 400
    
    try:
        async with current_app.async_session() as session:
            result = await session.execute(
                select(User).where(
                    (User.username == username) & 
                    (User.telegram_id == telegram_id)
                )
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid username or Telegram ID'
                }), 401
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'telegram_id': user.telegram_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'level': user.level,
                    'experience': user.experience,
                    'coins': user.coins
                }
            }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Login failed: {str(e)}'
        }), 500


@bp.route('/user/<int:telegram_id>', methods=['GET'])
@async_route
async def get_user(telegram_id):
    """Get user profile by Telegram ID"""
    from database.users import User
    from flask import current_app
    
    try:
        async with current_app.async_session() as session:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404
            
            return jsonify({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'telegram_id': user.telegram_id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'level': user.level,
                    'experience': user.experience,
                    'coins': user.coins,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch user: {str(e)}'
        }), 500
