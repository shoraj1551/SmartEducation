"""
SmartEducation - Flask Application
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from services.otp_service import mail
from routes.user_routes import user_bp
from routes.bookmark_routes import bookmark_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, static_folder='.')
    app.config.from_object(Config)
    
    # Configure session for temporary user storage
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(app, supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(bookmark_bp)
    
    # Serve static files
    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('.', path)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    print("=" * 50)
    print("SmartEducation Backend Server")
    print("=" * 50)
    host = app.config.get('HOST', 'localhost')
    port = app.config.get('PORT', 5000)
    print(f"Server running at: http://{host}:{port}")
    print(f"API Base URL: http://{host}:{port}/api")
    print("=" * 50)
    print("\n⚠️  NOTE: Email and SMS OTPs will NOT work until you configure credentials in .env")
    print("Follow CREDENTIALS_SETUP.md for instructions\n")
    app.run(
        host=host,
        port=port,
        debug=app.config.get('DEBUG', True)
    )


