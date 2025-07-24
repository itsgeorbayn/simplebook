from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import and_
from .message import Message

class Friendship(db.Model):
    __tablename__ = 'friendships'
    
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_accepted = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    def get_messages(self):
        user1_filter = (Message.sender == self.user1_id) | (Message.receiver == self.user1_id)
        user2_filter = (Message.sender == self.user2_id) | (Message.receiver == self.user2_id)
        
        return (
            db.session.query(Message)
            .filter(user1_filter & user2_filter, Message.is_deleted == False)
            .order_by(Message.sended_at)
            .all()
        )