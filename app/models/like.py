from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app.extensions import db
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
from app.utils import format_short_delta

class Like(db.Model):
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
    created_at = db.Column(db.DateTime, nullable=False)
    