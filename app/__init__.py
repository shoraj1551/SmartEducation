from flask import Flask
from flask_cors import CORS
from flask_session import Session
from .config import Config
from .services.otp_service import mail
import os

def create_app():
    """App Factory to create and configure the Flask application"""
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object(Config)
    
    # Configure session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    
    # Initialize extensions
    mail.init_app(app)
    CORS(app, supports_credentials=True)
    
    # MongoDB initialization
    from mongoengine import connect
    connect(host=app.config['MONGODB_SETTINGS']['host'])
    
    # Register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.user_routes import user_bp
    from .routes.bookmark_routes import bookmark_bp
    from .routes.inbox_routes import inbox_bp
    # from .routes.task_routes import tasks_bp
    from .routes.commitment_routes import commitment_bp
    from .routes.priority_routes import priority_bp
    from .routes.dashboard_routes import dashboard_bp
    from .routes.focus_routes import focus_bp
    from .routes.reality_routes import reality_bp
    from .routes.wellness_routes import wellness_bp
    from .routes.gamification_routes import gamification_bp
    from .routes.security_routes import security_bp
    from .routes.recall_routes import recall_bp
    from .routes.trigger_routes import trigger_bp
    from .routes.social_routes import social_bp
    from .routes.search_routes import search_bp
    from .routes.preference_routes import preference_bp
    from .routes.pod_routes import pod_bp
    from .routes.advanced_pod_routes import advanced_pod_bp
    from .routes.live_class_routes import live_class_bp
    from .routes.schedule_routes import schedule_bp
    # from .routes.video_guard_routes import video_guard_bp
    # from .routes.weekly_review_routes import weekly_review_bp
    # from .routes.burnout_routes import burnout_bp
    # from .routes.proof_routes import proof_bp
    from .routes.main_routes import main_bp
    # from .routes.admin_routes import admin_bp
    # from .routes.category_routes import category_bp
    # from .routes.learning_routes import learning_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(bookmark_bp)
    app.register_blueprint(inbox_bp)
    # app.register_blueprint(tasks_bp)
    app.register_blueprint(commitment_bp)
    app.register_blueprint(priority_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(focus_bp)
    app.register_blueprint(reality_bp)
    app.register_blueprint(wellness_bp)
    app.register_blueprint(gamification_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(recall_bp)
    app.register_blueprint(trigger_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(preference_bp)
    app.register_blueprint(pod_bp)
    app.register_blueprint(advanced_pod_bp)
    app.register_blueprint(live_class_bp)
    app.register_blueprint(schedule_bp)
    # app.register_blueprint(video_guard_bp)
    # app.register_blueprint(weekly_review_bp)
    # app.register_blueprint(burnout_bp)
    # app.register_blueprint(proof_bp)
    app.register_blueprint(main_bp)
    # app.register_blueprint(admin_bp)
    # app.register_blueprint(category_bp)
    # app.register_blueprint(learning_bp)

    return app
