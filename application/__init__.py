import os
import secrets
from flask import Flask

def create_app():
    """
    Create and configure the Flask application using the application factory pattern.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)

    # Configure the app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if not app.config['SECRET_KEY']:
        # Check if we're in production mode
        is_production = os.getenv('FLASK_ENV') == 'production'
        if is_production:
            raise ValueError("No SECRET_KEY set for production application")
        else:
            # For development only, generate a random key for this session
            # Note: This means sessions won't persist across server restarts
            app.logger.warning("No SECRET_KEY set, using randomly generated key for development")
            app.config['SECRET_KEY'] = secrets.token_hex(16)

    # Register blueprints
    from application.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.route('/test')
    def test_page():
        return "<h1>Test Page</h1>"

    return app