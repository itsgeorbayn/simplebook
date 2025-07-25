from app.extensions import db
from sqlalchemy.orm import relationship
from .comment import Comment
from .news import NewsItem
from datetime import datetime
from app.utils import format_short_delta

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String, unique=True, nullable=False)
    content = db.Column(db.String(4096), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime)
    
    is_edited = db.Column(db.Boolean, default=False)
    edited_at = db.Column(db.DateTime)
    
    is_reposted = db.Column(db.Boolean, default=False)
    reference = db.Column(db.Integer, db.ForeignKey('posts.id'))
    reposted_at = db.Column(db.DateTime)
    
    author = relationship('User', back_populates='post')
    comments = relationship('Comment', back_populates='post')
    
    def get_comments(self):
        return [({
            'id': comment.id,
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'picture': comment.author.picture,
            },
            'content': comment.content,
            'created_at': format_short_delta(datetime.now() - comment.created_at),
            'created_at_shorten': comment.created_at.strftime("%Y/%m/%d %I:%M %p"),
            'is_migrated': comment.is_migrated,
        }) for comment in self.comments if not comment.is_deleted]
    
    def mark_as_deleted(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()
        
        return self
    
    def mark_as_returned(self):
        self.is_deleted = False
        self.deleted_at = None
        
        return self
    
    def tag_as_reposted(self, id: int):
        self.is_reposted = True
        self.reference = id
        self.reposted_at = datetime.now()
        
        return self

    def find_updated_fields(self, form):
        potential_fields = {
            'title': self.title,
        }
        
        fields_to_update = dict()
        for field in potential_fields:
            if potential_fields[field] != form.get(field) and form.get(field) != "":
                fields_to_update.update({field: form.get(field)})

        return fields_to_update
    
    def send_news(self, return_news=False):
        author = self.author
        friends = author.friends
        
        news = db.session.query(NewsItem).filter(NewsItem.is_deleted == True, NewsItem.reference_table == 'posts', NewsItem.reference_id == self.id, NewsItem.recipient_id.in_(friends)).all()
        
        for item in news:
            item.mark_as_returned()
            friends.remove(item.recipient_id)
        db.session.commit()
        
        if not return_news:
            for friend in friends:
                news_item = NewsItem(title=f"New post by {author.username}", content="Your friend has recently posted new post! Come on and check it!", recipient_id=friend, reference_table='posts', reference_id=self.id)
                db.session.add(news_item)
            db.session.commit()
    
    def delete_news(self):
        author = self.author
        friends = author.friends
        
        news = db.session.query(NewsItem).filter(NewsItem.is_deleted == False, NewsItem.reference_table == 'posts', NewsItem.reference_id == self.id, NewsItem.recipient_id.in_(friends)).all()
        for news_item in news:
            news_item.mark_as_deleted()
        db.session.commit()
        
        return friends
    
    @property
    def created_at_shorten(self):
        return self.created_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def deleted_at_shorten(self):
        return self.deleted_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def edited_at_shorten(self):
        return self.edited_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def reposted_at_shorten(self):
        return self.reposted_at.strftime("%Y/%m/%d %I:%M %p")
    
    @property
    def reference_author(self):
        from .user import User
        
        if self.reference:
            return Post.query.get(self.reference).author.username