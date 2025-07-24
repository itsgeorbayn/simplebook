from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app.extensions import db
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta
from .news import NewsItem
from app.utils import format_short_delta

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    sender_user = relationship("User", foreign_keys=[sender], back_populates="sent_messages")
    receiver_user = relationship("User", foreign_keys=[receiver], back_populates="received_messages")
    
    content = db.Column(db.String, nullable=False)
    sended_at = db.Column(db.DateTime, nullable=False)
    
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime)
    
    is_forwarded = db.Column(db.Boolean, default=False)
    reference = db.Column(db.Integer, db.ForeignKey('messages.id'))
    forwarded_at = db.Column(db.DateTime)
    
    forwarded_message = relationship('Message', remote_side=[id], backref=backref('forwarded_by', lazy='dynamic'))
    
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'sender_username': self.sender_user.username,
            'sender_picture': self.sender_user.picture,
            'receiver': self.receiver,
            'content': self.content,
            'sended_at': self.sended_at.strftime("%Y/%m/%d %I:%M %p"),
            'is_forwarded': self.is_forwarded,
            'forwarded_message_author': self.forwarded_message.sender_user.username if self.is_forwarded else None,
            'forwarded_message_author_picture': self.forwarded_message.sender_user.picture if self.is_forwarded else None,
            'forwarded_at': self.forwarded_at.strftime("%Y/%m/%d %I:%M %p") if self.forwarded_at else None,
            'is_edited': self.is_edited,
            'edited_at_shorten': format_short_delta(datetime.now() - self.edited_at) if self.is_edited else None,
            'edited_at': self.edited_at.strftime("%Y/%m/%d %I:%M %p") if self.is_edited else None
        }
        
    def send_news(self):
        news_item = db.session.query(NewsItem).filter(
            NewsItem.is_deleted == False, 
            NewsItem.reference_table == 'messages', 
            NewsItem.reference_id.in_([m.id for m in self.sender_user.sent_messages])
        ).first()
        
        if news_item:
            news_item.content = f"Your friend has recently sended you few messages! Come on and check them!"
        else:
            news_item = NewsItem(title=f"New message by {self.sender_user.username}", content="Your friend has recently sended you a message! Come on and check it!", recipient_id=self.receiver, reference_table='messages', reference_id=self.id)
            db.session.add(news_item)
        db.session.commit()
    
    def tag_as_forwarded(self, id: int):
        self.is_forwarded = True
        self.reference = id
        self.forwarded_at = datetime.now().strftime("%Y/%m/%d %I:%M %p")
        
        return self
    
    def tag_as_edited(self):
        self.is_edited = True
        self.edited_at = datetime.now().strftime("%Y/%m/%d %I:%M %p")
        
        return self
    
    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        
        return self
    
    def mark_as_returned(self):
        self.is_deleted = False
        self.deleted_at = None
        
        return self
    
    @property
    def deleted_at_shorten(self):
        return self.deleted_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def edited_at_shorten(self):
        return self.edited_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def forwarded_at_shorten(self):
        return self.forwarded_at.strftime("%Y/%m/%d %I:%M %p")