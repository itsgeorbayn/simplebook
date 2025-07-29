from flask import Flask, jsonify, session, request
from flask_migrate import Migrate
import sys, os, logging
from .routes import *
from .extensions import db, jwt, login_manager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.DEBUG)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify(error=str(e)), 500
    
    @app.before_request
    def track_history():
        if 'history' not in session:
            session['history'] = []
            
        if not request.path.startswith('/static') and not request.path.startswith('/messages/live') and 'favicon.ico' not in request.path:
            session['history'].append(request.full_path)
            session['history'] = session['history'][-10:]
            
    @app.context_processor
    def inject_common_template_variables():
        return dict(history=session.get('history', []))

    app.jinja_env.globals['getattr'] = getattr  
    
    app.config.from_object(Config)
    
    for bp in (auth_bp, profile_bp, posts_bp, index_bp, friends_bp, messages_handler_bp, admin_bp):
        app.register_blueprint(bp)
    
    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login_form'
    login_manager.login_message = 'You must be logged in to access this page.'
    login_manager.login_message_category = 'warning'
    
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()

    return app