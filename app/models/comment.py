from app.extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    content = db.Column(db.String(4096), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime)
    
    is_migrated = db.Column(db.Boolean, default=False)
    
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')
    
    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
            
        return self
    
    def mark_as_returned(self):
        self.is_deleted = False
        self.deleted_at = None
            
        return self
    
    @property
    def created_at_shorten(self):
        return self.created_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def deleted_at_shorten(self):
        return self.deleted_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def edited_at_shorten(self):
        return self.edited_at.strftime("%Y/%m/%d %I:%M %p")