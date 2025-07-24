from flask import Flask, jsonify
from flask_migrate import Migrate
import sys, os, logging
from .routes import *
from .extensions import db, jwt, login_manager
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    logging.basicConfig(level=logging.DEBUG)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify(error=str(e)), 500
    
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