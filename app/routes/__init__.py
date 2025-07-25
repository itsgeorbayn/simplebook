from .auth import auth_bp
from .profile import profile_bp
from .posts import posts_bp
from .index import index_bp
from .friends import friends_bp
from .messages_handler import messages_handler_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'profile_bp', 'posts_bp', 'index_bp', 'friends_bp', 'messages_handler_bp', 'admin_bp']