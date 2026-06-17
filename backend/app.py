"""
LifeQuest Web Server - Flask API for RPG Game
"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.users import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['ENV'] = os.getenv('ENV', 'development')
app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./bot.db')
async_db_url = DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")

# Store session maker for use in routes
app.engine = None
app.async_session = None


async def init_db():
    """Initialize database connection"""
    app.engine = create_async_engine(async_db_url, echo=False)
    app.async_session = sessionmaker(app.engine, class_=AsyncSession, expire_on_commit=False)
    
    async with app.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


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
    import asyncio
    
    # Initialize database
    asyncio.run(init_db())
    
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )


if __name__ == '__main__':
    run_server()
