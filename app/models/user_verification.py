from app.extensions import db
from sqlalchemy.orm import relationship
from .comment import Comment
import uuid
from datetime import datetime, timedelta

class UserVerification(db.Model):
    __tablename__ = 'user_verifications'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    verification_code = db.Column(db.String(6), nullable=False)
    code_expiration = db.Column(db.DateTime, nullable=False)
    
    @classmethod
    def new(cls, user_id):
        expiration = datetime.now() + timedelta(hours=1)
        return UserVerification(user_id=user_id, verification_code=uuid.uuid4().hex[:6].upper(), code_expiration=expiration)