"""
Authentication API routes — Flask Blueprint for the LifeQuest Mini App backend.

This module exposes RESTful endpoints under /api/auth/ that handle Telegram
Mini App session resolution, character registration (both via Telegram login
and legacy username/password), login, account deletion, and profile retrieval.

Architectural notes:
- The blueprint is registered in backend/app.py with url_prefix='/api/auth'.
- All endpoints that need database access obtain a session factory from the
  Flask app object via get_session_factory() -> current_app.session_local.
- The shared User model (database/users.py) is imported lazily inside each
  route function to avoid circular import issues and module-level coupling.
- Telegram initData (from the Mini App frontend) is cryptographically verified
  using the BOT_TOKEN before any database operation is performed.
"""

from flask import Blueprint, request, jsonify
from sqlalchemy import func, select
import hashlib
import hmac
import json
import os
from urllib.parse import parse_qsl

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ---------------------------------------------------------------------------
# Telegram initData verification helpers
# ---------------------------------------------------------------------------


def get_bot_token() -> str:
    """
    Read the BOT_TOKEN from the environment.

    Raises RuntimeError if the token is missing or empty. Used by
    verify_telegram_init_data to compute the expected HMAC signature.
    """
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        raise RuntimeError('BOT_TOKEN is not configured')
    return token


def verify_telegram_init_data(init_data: str) -> dict:
    """
    Validate Telegram Mini App initData and return the Telegram user payload.

    Telegram Mini Apps send an initData string (URL-encoded query parameters)
    containing the authenticated user and a cryptographic hash. This function:
    1. Parses the query string into key-value pairs.
    2. Pops the 'hash' parameter — this is the expected signature.
    3. Sorts the remaining pairs and joins them with newlines.
    4. Derives a secret key via HMAC-SHA256(WebAppData, bot_token).
    5. Computes an HMAC-SHA256(secret_key, data_check_string).
    6. Compares the computed hash with the received hash (constant-time).
    7. Deserialises the 'user' JSON payload and returns it.

    Raises ValueError if any step fails (missing data, invalid signature).
    """
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


# ---------------------------------------------------------------------------
# Username and password helpers
# The following functions mirror the same utilities in handlers/start.py.
# Both the Telegram bot and the web server need them, so they are duplicated
# rather than creating a shared helper module. A future refactor should
# extract them into a common utils package.
# ---------------------------------------------------------------------------


def normalize_username(username: str) -> str:
    """Normalize a username for consistent lookup: strip whitespace,
    remove leading '@', and convert to lowercase."""
    return username.strip().lstrip('@').lower()


def validate_username(username: str) -> str | None:
    """
    Validate a proposed username and return an error message if invalid.

    Rules:
    - Must be between 3 and 20 characters.
    - May only contain letters, digits, hyphens, and underscores.
    Returns None when the username is valid.
    """
    if len(username) < 3 or len(username) > 20:
        return 'Username must be 3-20 characters'

    if not username.replace('_', '').replace('-', '').isalnum():
        return 'Username can only contain letters, numbers, hyphens, and underscores'

    return None


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with a random 16-byte salt.

    Output format: "<salt_hex>$<hash_hex>" — stored in User.password_hash.
    Uses 600 000 iterations for reasonable brute-force resistance.
    """
    salt = os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        600_000,
    )
    return f'{salt.hex()}${password_hash.hex()}'


def verify_password(password: str, stored_hash: str | None) -> bool:
    """
    Verify a password against its stored hash.

    Supports two formats:
    - New format: "<salt_hex>$<hash_hex>" (PBKDF2-HMAC-SHA256).
    - Legacy format: plain SHA256 hex string (used before migration).
    Also handles the special "telegram$..." prefix — these hashes belong to
    Telegram-only accounts that never set a password; verification returns False.
    Returns False for any None, empty, or malformed stored hash.
    """
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


# ---------------------------------------------------------------------------
# Serialisation helpers
# ---------------------------------------------------------------------------


def serialize_user(user):
    """
    Convert a User SQLAlchemy model instance into a JSON-safe dictionary.

    This is the standard shape returned to the frontend for all authenticated
    endpoints. Timestamps are serialised as ISO-8601 strings.
    """
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
    """
    Extract a safe subset of Telegram user fields for the frontend.

    This intentionally excludes sensitive fields (e.g. 'allows_write_to_pm')
    and returns only what the UI needs for display and personalisation.
    """
    return {
        'id': telegram_user.get('id'),
        'username': telegram_user.get('username'),
        'first_name': telegram_user.get('first_name', ''),
        'last_name': telegram_user.get('last_name', ''),
        'language_code': telegram_user.get('language_code'),
        'photo_url': telegram_user.get('photo_url'),
    }


def make_unusable_password_hash() -> str:
    """
    Generate a password hash that can never be verified.

    Used for Telegram-only accounts (registered via the Mini App) that do not
    set a password. The "telegram$" prefix causes verify_password() to always
    return False, effectively disabling legacy username/password login for
    these accounts.
    """
    return f"telegram${os.urandom(32).hex()}"


# ---------------------------------------------------------------------------
# Database session helper
# ---------------------------------------------------------------------------


def get_session_factory():
    """
    Retrieve the SQLAlchemy session factory from the Flask app context.

    The factory is attached to current_app.session_local by backend/app.py's
    init_db() function. This indirection keeps route handlers decoupled from
    the global app object and makes them usable with any Flask app instance
    that has been properly initialised.

    Returns a sessionmaker bound to the same engine used by the bot (main.py).
    """
    from flask import current_app

    if current_app.session_local is None:
        raise RuntimeError("Database not initialized")

    return current_app.session_local


# ===========================================================================
# Route: Telegram Mini App session resolution
# ===========================================================================


@bp.route('/telegram/session', methods=['POST'])
def telegram_session():
    """
    Resolve the current Telegram Mini App session.

    This is the first endpoint called by the frontend after the Mini App opens.
    It verifies the Telegram initData, looks up the User by telegram_id, and
    tells the frontend whether this Telegram user is already registered.

    Expected request body: { "init_data": "..." }
    Response:
    - 200 with {"registered": true/false, "telegram_user": {...}, "user": ...}
    - 401 if initData is missing, malformed, or the signature is invalid.
    """
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


# ===========================================================================
# Route: Telegram Mini App character registration
# ===========================================================================


@bp.route('/telegram/register', methods=['POST'])
def telegram_register():
    """
    Create a new RPG character linked to a Telegram account.

    Flow:
    1. Verify the Telegram initData and extract the user profile.
    2. Validate the chosen username (3-20 chars, alphanumeric + hyphens/underscores).
    3. Check for duplicate telegram_id or username.
    4. Create a User row with a non-usable password hash (Telegram-only account).
    5. Return the serialised user to the frontend.

    Expected request body:
    {
        "init_data": "...",
        "username": "hero_name",
        "display_name": "Hero Name",
        "character_class": "warrior",
        "avatar": "pixel_warrior"
    }
    Responses: 201 (created), 200 (already exists), 400 (validation), 409 (conflict).
    """
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


# ===========================================================================
# Route: Legacy username/password registration
# ===========================================================================


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user with a username and password (legacy flow).

    This endpoint is used when a user registers via the Mini App but wants
    a full password-based account (unlike /telegram/register which creates
    a Telegram-only account without a usable password).

    Expected JSON:
    {
        "username": "username",
        "password": "password",
        "telegram_id": 123456789,
        "first_name": "John",
        "last_name": "Doe"
    }

    Responses: 201 (created), 400 (validation), 409 (duplicate username/telegram_id).
    """
    from database.users import User
    
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


# ===========================================================================
# Route: Legacy username/password login
# ===========================================================================


@bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user with username and password (legacy flow).

    Flow:
    1. Look up the user by normalized username.
    2. Verify the password against the stored hash.
    3. If the user already has a telegram_id and it differs from the request,
       reject with 403 (account already linked to another Telegram user).
    4. If the user has no telegram_id or it matches, link/update it and commit.
    5. Return the serialised user.

    Expected JSON:
    {
        "username": "username",
        "password": "password",
        "telegram_id": 123456789
    }

    Responses: 200 (success), 401 (invalid credentials), 403 (already linked).
    """
    from database.users import User
    
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


# ===========================================================================
# Route: Account deletion
# ===========================================================================


@bp.route('/account', methods=['DELETE'])
def delete_account():
    """
    Permanently delete a user account after confirming username and password.

    Flow:
    1. Validate that username and password are present (password must be a string).
    2. Look up the user by normalized username (supports bare and @username form).
    3. Verify the password against the stored hash.
    4. Delete the User row and commit.

    Expected JSON:
    {
        "username": "username",
        "password": "password"
    }

    Responses: 200 (deleted), 400 (missing fields), 401 (invalid credentials).
    """
    from database.users import User

    data = request.get_json()

    if not data:
        return jsonify({'status': 'error', 'message': 'No JSON data provided'}), 400

    username = normalize_username(data.get('username', ''))
    password = data.get('password', '')

    if not isinstance(password, str):
        return jsonify({
            'status': 'error',
            'message': 'Password must be a string'
        }), 400

    if not username or not password:
        return jsonify({
            'status': 'error',
            'message': 'Username and password are required'
        }), 400

    try:
        with get_session_factory()() as session:
            username_column = func.lower(func.trim(User.username))
            user = session.execute(
                select(User).where(
                    username_column.in_((username, f'@{username}'))
                )
            ).scalar_one_or_none()

            if not user or not verify_password(password, user.password_hash):
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid username or password'
                }), 401

            deleted_user = {
                'id': user.id,
                'username': user.username,
            }

            session.delete(user)
            session.commit()

            return jsonify({
                'status': 'success',
                'message': 'Account deleted successfully',
                'deleted_user': deleted_user
            }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Account deletion failed: {str(e)}'
        }), 500


# ===========================================================================
# Route: User profile lookup
# ===========================================================================


@bp.route('/user/<int:telegram_id>', methods=['GET'])
def get_user(telegram_id):
    """
    Fetch a user profile by Telegram ID.

    This is a read-only endpoint used by the frontend to display character
    information after a session has been established.

    Responses: 200 (found), 404 (not found).
    """
    from database.users import User
    
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