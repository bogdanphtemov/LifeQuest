"""
LifeQuest Web Server - Flask API for RPG Game
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

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.users import Base

load_dotenv()

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# --- Rate Limiter ---
# Використовуємо in-memory storage (для SQLite/dev підходить).
# Для продакшну з PostgreSQL варто використати Redis:
#   storage_uri="redis://localhost:6379"
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
    # Apply Alembic migrations (безпечні DDL замість сирого SQL)
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '..', 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')



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
