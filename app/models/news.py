from app.extensions import db
from sqlalchemy.orm import relationship
from .comment import Comment
from datetime import datetime
from app.utils import format_short_delta

class NewsItem(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.now())
    
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime)
    
    reference_table = db.Column(db.String)
    reference_id = db.Column(db.Integer)
    
    recipient = relationship('User', back_populates='news')
    
    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        
        return self
    
    def mark_as_returned(self):
        self.is_deleted = False
        self.deleted_at = None
        
        return self
    
    @property
    def last_update_shorten(self):
        return self.last_update.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def deleted_at_shorten(self):
        return self.deleted_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def reference_author(self):
        from .post import Post
        from .message import Message
        
        cls = {
            'posts': {
                'name': Post,
                'attr': 'author'
            },
            'messages': {
                'name': Message,
                'attr': 'sender_user'
            }
        }
        author = getattr(db.session.get(cls[self.reference_table]['name'], self.reference_id), cls[self.reference_table]['attr'])
        return author