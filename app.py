"""
SmartEducation - Flask Application
"""
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from models import User
from services.otp_service import mail
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.bookmark_routes import bookmark_bp
from routes.inbox_routes import inbox_bp
from routes.task_routes import tasks_bp
from routes.commitment_routes import commitments_bp
from routes.priority_routes import priority_bp
from routes.focus_routes import focus_bp
from routes.reality_routes import reality_bp
from routes.video_guard_routes import video_guard_bp
from routes.weekly_review_routes import weekly_review_bp
from routes.burnout_routes import burnout_bp
from routes.proof_routes import proof_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, static_folder='.')
    app.config.from_object(Config)
    
    # Configure session for temporary user storage
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    
    # Initialize extensions
    mail.init_app(app)
    CORS(app, supports_credentials=True)
    
    # MongoDB handles collection creation automatically
    from mongoengine import connect
    connect(host=app.config['MONGODB_SETTINGS']['host'])
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bookmark_bp)
    app.register_blueprint(inbox_bp)  # NEW: Unified Learning Inbox routes
    app.register_blueprint(tasks_bp)  # NEW: Task generation routes
    app.register_blueprint(commitments_bp)  # NEW: Commitment routes
    app.register_blueprint(priority_bp)  # NEW: Priority engine routes
    app.register_blueprint(focus_bp)  # NEW: Focus mode routes
    app.register_blueprint(reality_bp)  # NEW: Reality metrics routes
    app.register_blueprint(video_guard_bp)  # NEW: Video guard routes
    app.register_blueprint(weekly_review_bp)  # NEW: Weekly review routes
    app.register_blueprint(burnout_bp)  # NEW: Burnout detection routes
    app.register_blueprint(proof_bp)  # NEW: Proof-of-learning routes

    
    # Serve static files
    @app.route('/')
    def index():
        return send_from_directory('.', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('.', path)
    
    # MongoDB handles collection creation automatically
    
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


