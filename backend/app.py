"""
LifeQuest Web Server — Flask API for the Telegram Mini App.

This module is the entry point of the Flask web application that powers the
Telegram Mini App frontend. It configures the Flask app, initialises the
database (via SQLAlchemy), registers API blueprints, serves static frontend
assets, and handles top-level error responses.

Architectural overview:
- Flask serves a single-page application (SPA) from the frontend/ directory.
- API routes are grouped under Blueprints (e.g. /api/auth/*) defined in
  backend/routes/.
- The database engine and session factory are attached to app.engine and
  app.session_local so they are accessible to route modules via Flask's
  current_app proxy.
- The same SQLAlchemy User model (database/users.py) is shared with the
  Telegram bot (main.py), ensuring data consistency.

Note on project structure:
- backend/app.py uses sys.path.insert to allow importing shared modules
  (database/, config.py) from the project root. This is a recognised
  anti-pattern; a production-ready solution would use a setup.py /
  pyproject.toml installable package or PYTHONPATH. For a development
  pet project this approach is pragmatic.
"""

import os
import sys
from flask import Flask, abort, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

# Prepend the project root to sys.path so that shared modules (config.py,
# database/, handlers/) can be imported consistently from both the bot
# (main.py) and the web server (backend/app.py).
# In a production setup this would be replaced by an installable package.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.users import Base

load_dotenv()

# Absolute path to the frontend directory, used for serving static assets
# and the SPA entry point (index.html).
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# --- Rate Limiter ---
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
    enabled=True,
)

# Configuration
app.config['ENV'] = os.getenv('ENV', 'development')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./bot.db')

# Placeholders — populated by init_db() before routes are used.
# Stored on the app object so route blueprints can retrieve them via
# current_app.session_local. See backend/routes/auth_routes.py's
# get_session_factory() for the consumer side.
app.engine = None
app.session_local = None


def init_db():
    """
    Create the database engine and session factory, and ensure all tables
    (including the shared User model) exist.

    Call this once at startup before registering blueprints or handling requests.
    """
    app.engine = create_engine(DATABASE_URL, echo=False)
    app.session_local = sessionmaker(
        bind=app.engine,
        class_=Session,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=app.engine)
    migrate_sqlite_schema()


def migrate_sqlite_schema():
    """
    Apply additive migrations to an existing SQLite database.

    During development the User model gained new columns (password_hash,
    display_name, avatar, character_class). This function checks the current
    schema and adds any missing columns, allowing local SQLite databases to
    work without a full migration framework.

    This is a no-op for non-SQLite databases and for fresh databases whose
    schema is already up to date.
    """
    if app.engine is None or app.engine.dialect.name != 'sqlite':
        return

    inspector = inspect(app.engine)
    if 'users' not in inspector.get_table_names():
        return

    existing_columns = {column['name'] for column in inspector.get_columns('users')}
    migrations = {
        'password_hash': 'ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)',
        'display_name': 'ALTER TABLE users ADD COLUMN display_name VARCHAR(255)',
        'avatar': (
            "ALTER TABLE users ADD COLUMN avatar VARCHAR(64) "
            "DEFAULT 'pixel_adventurer'"
        ),
        'character_class': (
            "ALTER TABLE users ADD COLUMN character_class VARCHAR(64) "
            "DEFAULT 'adventurer'"
        ),
        'texture_path': 'ALTER TABLE users ADD COLUMN texture_path VARCHAR(512)',
        'sprite_data': 'ALTER TABLE users ADD COLUMN sprite_data TEXT',
    }

    with app.engine.begin() as connection:
        for column_name, statement in migrations.items():
            if column_name not in existing_columns:
                connection.execute(text(statement))


# Import routes
from backend.routes import auth_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health-check endpoint.

    Returns a simple JSON response confirming the server is alive. Useful for
    monitoring and for verifying that the Flask app starts without errors.
    """
    return jsonify({
        'status': 'ok',
        'message': 'LifeQuest Web Server is running',
        'version': '0.1.0'
    }), 200


@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve the Telegram Mini App entry point (index.html)."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_static_asset(path):
    """
    Serve frontend static assets (CSS, JS, images) with SPA fallback.

    Security: path traversal is mitigated by normalising the path and
    verifying it does not escape FRONTEND_DIR before passing it to
    send_from_directory (which itself uses Flask's safe_join internally).

    Behaviour:
    - If the requested path begins with 'api/', abort with 404 (API routes
      are handled by blueprints, not by this catch-all).
    - If the normalised path stays within FRONTEND_DIR and matches an actual
      file, serve it.
    - Otherwise, serve index.html (SPA fallback — the frontend router
      handles client-side navigation).
    """
    if path.startswith('api/'):
        abort(404)

    # Guard against path traversal attacks (e.g. /../../../etc/passwd).
    safe_path = os.path.normpath('/' + path).lstrip('/')
    target = os.path.join(FRONTEND_DIR, safe_path)
    real_target = os.path.realpath(target)
    real_frontend = os.path.realpath(FRONTEND_DIR)

    if os.path.isfile(target) and real_target.startswith(real_frontend):
        return send_from_directory(FRONTEND_DIR, safe_path)

    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.errorhandler(404)
def not_found(error):
    """Return a JSON error for 404 (endpoint not found)."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Return a JSON error for 500 (internal server error)."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


def run_server():
    """
    Initialise the database and start the Flask development server.

    The server binds to 0.0.0.0 so it is reachable from outside the container
    (e.g. via ngrok for Telegram Mini App development). The port defaults to
    5000 and can be overridden with the PORT environment variable.
    """
    init_db()
    
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    run_server()
