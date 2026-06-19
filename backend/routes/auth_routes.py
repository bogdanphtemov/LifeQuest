"""
Authentication API routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import select
import hashlib
import hmac
import json
import os
from urllib.parse import parse_qsl

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def get_bot_token() -> str:
    """Read the bot token required to validate Telegram Mini App data."""
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        raise RuntimeError('BOT_TOKEN is not configured')
    return token


def verify_telegram_init_data(init_data: str) -> dict:
    """Validate Telegram Mini App initData and return the Telegram user."""
    if not init_data:
        raise ValueError('Telegram initData is required')

    parsed_data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed_data.pop('hash', None)
    if not received_hash:
        raise ValueError('Telegram initData hash is missing')

    data_check_string = '\n'.join(
        f'{key}={value}' for key, value in sorted(parsed_data.items())
    )
    secret_key = hmac.new(
        b'WebAppData',
        get_bot_token().encode('utf-8'),
        hashlib.sha256,
    ).digest()
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise ValueError('Telegram initData signature is invalid')

    if 'user' not in parsed_data:
        raise ValueError('Telegram user data is missing')

    return json.loads(parsed_data['user'])


def normalize_username(username: str) -> str:
    """Normalize username for consistent login lookup."""
    return username.strip().lower()


def validate_username(username: str) -> str | None:
    """Return an error message when username is invalid."""
    if len(username) < 3 or len(username) > 20:
        return 'Username must be 3-20 characters'

    if not username.replace('_', '').replace('-', '').isalnum():
        return 'Username can only contain letters, numbers, hyphens, and underscores'

    return None


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC with a per-user salt."""
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        600_000,
    )
    return f'{salt.hex()}${password_hash.hex()}'


def verify_password(password: str, stored_hash: str | None) -> bool:
    """Verify a password against supported stored hash formats."""
    if not stored_hash:
        return False

    if '$' not in stored_hash:
        legacy_hash = hashlib.sha256(password.encode()).hexdigest()
        return hmac.compare_digest(legacy_hash, stored_hash)

    salt_hex, hash_hex = stored_hash.split('$', 1)
    if salt_hex == 'telegram':
        return False

    try:
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        600_000,
    )
    return hmac.compare_digest(password_hash.hex(), hash_hex)


def serialize_user(user):
    """Serialize user model for API responses."""
    return {
        'id': user.id,
        'telegram_id': user.telegram_id,
        'username': user.username,
        'display_name': user.display_name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'avatar': user.avatar,
        'character_class': user.character_class,
        'level': user.level,
        'experience': user.experience,
        'coins': user.coins,
        'created_at': user.created_at.isoformat() if user.created_at else None,
    }


def serialize_telegram_user(telegram_user):
    """Expose only the Telegram user fields needed by the frontend."""
    return {
        'id': telegram_user.get('id'),
        'username': telegram_user.get('username'),
        'first_name': telegram_user.get('first_name', ''),
        'last_name': telegram_user.get('last_name', ''),
        'language_code': telegram_user.get('language_code'),
        'photo_url': telegram_user.get('photo_url'),
    }


def make_unusable_password_hash() -> str:
    """Create a password hash value for Telegram-only accounts."""
    return f"telegram${os.urandom(32).hex()}"


def get_session_factory():
    """Get database session from Flask app context"""
    from flask import current_app

    if current_app.session_local is None:
        raise RuntimeError("Database not initialized")

    return current_app.session_local


@bp.route('/telegram/session', methods=['POST'])
def telegram_session():
    """Resolve the current Telegram Mini App session."""
    from database.users import User

    data = request.get_json() or {}

    try:
        telegram_user = verify_telegram_init_data(data.get('init_data', ''))
    except (ValueError, json.JSONDecodeError) as error:
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 401

    telegram_id = telegram_user.get('id')
    if not telegram_id:
        return jsonify({
            'status': 'error',
            'message': 'Telegram user id is missing'
        }), 401

    try:
        with get_session_factory()() as session:
            user = session.execute(
                select(User).where(User.telegram_id == telegram_id)
            ).scalar_one_or_none()

            return jsonify({
                'status': 'success',
                'registered': user is not None,
                'telegram_user': serialize_telegram_user(telegram_user),
                'user': serialize_user(user) if user else None,
            }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to resolve Telegram session: {str(e)}'
        }), 500


@bp.route('/telegram/register', methods=['POST'])
def telegram_register():
    """Create a Telegram-linked RPG character."""
    from database.users import User

    data = request.get_json() or {}

    try:
        telegram_user = verify_telegram_init_data(data.get('init_data', ''))
    except (ValueError, json.JSONDecodeError) as error:
        return jsonify({
            'status': 'error',
            'message': str(error)
        }), 401

    telegram_id = telegram_user.get('id')
    if not telegram_id:
        return jsonify({
            'status': 'error',
            'message': 'Telegram user id is missing'
        }), 401

    username = normalize_username(data.get('username', ''))
    display_name = data.get('display_name', '').strip()
    character_class = data.get('character_class', 'adventurer').strip() or 'adventurer'
    avatar = data.get('avatar', 'pixel_adventurer').strip() or 'pixel_adventurer'

    validation_error = validate_username(username)
    if validation_error:
        return jsonify({
            'status': 'error',
            'message': validation_error
        }), 400

    try:
        with get_session_factory()() as session:
            existing_telegram_user = session.execute(
                select(User).where(User.telegram_id == telegram_id)
            ).scalar_one_or_none()
            if existing_telegram_user:
                return jsonify({
                    'status': 'success',
                    'message': 'User already registered',
                    'user': serialize_user(existing_telegram_user)
                }), 200

            existing_username = session.execute(
                select(User).where(User.username == username)
            ).scalar_one_or_none()
            if existing_username:
                return jsonify({
                    'status': 'error',
                    'message': 'Username already exists'
                }), 409

            new_user = User(
                telegram_id=telegram_id,
                username=username,
                password_hash=make_unusable_password_hash(),
                display_name=display_name or telegram_user.get('first_name') or username,
                first_name=telegram_user.get('first_name', ''),
                last_name=telegram_user.get('last_name', ''),
                avatar=avatar,
                character_class=character_class,
                level=1,
                experience=0,
                coins=0,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

            return jsonify({
                'status': 'success',
                'message': 'Character created successfully',
                'user': serialize_user(new_user)
            }), 201

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Character creation failed: {str(e)}'
        }), 500


@bp.route('/register', methods=['POST'])
def register():
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
    username = normalize_username(data.get('username', ''))
    password = data.get('password', '').strip()
    telegram_id = data.get('telegram_id')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    validation_error = validate_username(username)
    if validation_error:
        return jsonify({
            'status': 'error',
            'message': validation_error
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
        with get_session_factory()() as session:
            # Check if user already exists
            result = session.execute(
                select(User).where(User.username == username)
            )
            if result.scalar_one_or_none():
                return jsonify({
                    'status': 'error',
                    'message': 'Username already exists'
                }), 409
            
            # Check if telegram_id already exists
            result = session.execute(
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
                password_hash=hash_password(password),
                display_name=first_name or username,
                first_name=first_name,
                last_name=last_name,
                avatar='pixel_adventurer',
                character_class='adventurer',
                level=1,
                experience=0,
                coins=0,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            
            return jsonify({
                'status': 'success',
                'message': 'User registered successfully',
                'user': serialize_user(new_user)
            }), 201
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Registration failed: {str(e)}'
        }), 500


@bp.route('/login', methods=['POST'])
def login():
    """Login user
    
    Expected JSON:
    {
        "username": "username",
        "password": "password",
        "telegram_id": 123456789
    }
    """
    from database.users import User
    from flask import current_app
    
    data = request.get_json()
    
    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400
    
    username = normalize_username(data.get('username', ''))
    password = data.get('password', '').strip()
    telegram_id = data.get('telegram_id')
    
    if not username or not password or not telegram_id:
        return jsonify({
            'status': 'error',
            'message': 'Username, password, and Telegram ID are required'
        }), 400
    
    try:
        with get_session_factory()() as session:
            result = session.execute(
                select(User).where(User.username == username)
            )
            user = result.scalar_one_or_none()
            
            if not user or not verify_password(password, user.password_hash):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid username or password'
                }), 401

            if user.telegram_id and user.telegram_id != telegram_id:
                return jsonify({
                    'status': 'error',
                    'message': 'Account is linked to another Telegram user'
                }), 403

            if user.telegram_id != telegram_id:
                user.telegram_id = telegram_id
                session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'user': serialize_user(user)
            }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Login failed: {str(e)}'
        }), 500


@bp.route('/user/<int:telegram_id>', methods=['GET'])
def get_user(telegram_id):
    """Get user profile by Telegram ID"""
    from database.users import User
    from flask import current_app
    
    try:
        with get_session_factory()() as session:
            result = session.execute(
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
                'user': serialize_user(user)
            }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to fetch user: {str(e)}'
        }), 500
