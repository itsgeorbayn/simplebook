from app.extensions import db
from sqlalchemy.orm import relationship

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    content = db.Column(db.String, nullable=False)
    
    post = relationship('Post', back_populates='tags')