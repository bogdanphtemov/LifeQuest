"""
LifeQuest Web Server - Flask API for RPG Game
"""
import os
import sys
from flask import Flask, abort, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.users import Base

load_dotenv()

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# Configuration
app.config['ENV'] = os.getenv('ENV', 'development')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./bot.db')

# Store session maker for use in routes
app.engine = None
app.session_local = None


def init_db():
    """Initialize database connection"""
    app.engine = create_engine(DATABASE_URL, echo=False)
    app.session_local = sessionmaker(
        bind=app.engine,
        class_=Session,
        expire_on_commit=False,
    )
    Base.metadata.create_all(bind=app.engine)
    migrate_sqlite_schema()


def migrate_sqlite_schema():
    """Add missing SQLite columns for existing local development databases."""
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
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'LifeQuest Web Server is running',
        'version': '0.1.0'
    }), 200


@app.route('/', methods=['GET'])
def serve_frontend():
    """Serve the Telegram Mini App shell."""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_static_asset(path):
    """Serve frontend assets and fall back to the app shell."""
    if path.startswith('api/'):
        abort(404)

    target = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(target):
        return send_from_directory(FRONTEND_DIR, path)

    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


def run_server():
    """Run Flask server"""
    init_db()
    
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    run_server()
