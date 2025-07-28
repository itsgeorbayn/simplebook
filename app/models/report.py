from app.extensions import db
from sqlalchemy.orm import relationship
from .comments import Comment
from .news import NewsItem
from .post import Post
from datetime import datetime
from app.utils import format_short_delta

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = relationship('User', back_populates='reports')
    
    reference_table = db.Column(db.String)
    reference_id = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    
    _translate = {
        "posts": {"name": Post, "delete_endpoint": "admin.delete_post_form"},
        "comments": {"name": Comment, "delete_endpoint": "admin.delete_comment_form"}
    }

    @property
    def created_at_shorten(self):
        return self.created_at.strftime("%Y/%m/%d %I:%M %p")
        
    @property
    def target(self):
        obj = db.session.get(self._translate.get(self.reference_table).get("name"), self.reference_id)
        return obj if obj else None
    
    @property
    def delete_endpoint(self):
        return self._translate.get(self.reference_table).get("delete_endpoint")