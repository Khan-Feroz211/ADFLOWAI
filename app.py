"""
ADFLOWAI - Main Application Entry Point
AI-Powered Multi-Platform Campaign Optimization System

Author: Khan Feroz
License: MIT
"""

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import configurations
from config.settings import Config
from src.core.database import init_db
from src.api.routes import register_blueprints

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Application factory pattern
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    jwt = JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register API blueprints
    register_blueprints(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring"""
        return jsonify({
            'status': 'healthy',
            'service': 'ADFLOWAI',
            'version': '1.0.0'
        }), 200
    
    # Root endpoint
    @app.route('/')
    def index():
        """Root endpoint with API information"""
        return jsonify({
            'service': 'ADFLOWAI API',
            'version': '1.0.0',
            'description': 'AI-Powered Multi-Platform Campaign Optimization',
            'endpoints': {
                'health': '/health',
                'api': '/api/v1',
                'docs': '/api/docs'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info("ADFLOWAI application initialized successfully")
    return app


# Create application instance
app = create_app()


if __name__ == '__main__':
    # Development server
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    logger.info(f"Starting ADFLOWAI server on port {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
