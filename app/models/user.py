from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures.file_storage import FileStorage
from flask_login import UserMixin, current_user
from flask import current_app
from app.extensions import db
from sqlalchemy.orm import relationship, column_property, foreign, aliased
from sqlalchemy import desc, case, select, func, and_, or_
from datetime import datetime, timedelta
from app.utils import format_short_delta, flatten
from .comments import Comment
from .report import Report
from .friendship import Friendship
from .admin_permissions import AdminPermission
from .like import Like
from .post import Post
from .news import NewsItem

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    picture = db.Column(db.String, default='default.png')

    is_banned = db.Column(db.Boolean, default=False)
    banned_at = db.Column(db.DateTime)
    
    sent_messages = relationship("Message", foreign_keys="[Message.sender]", back_populates="sender_user")
    received_messages = relationship("Message", foreign_keys="[Message.receiver]", back_populates="receiver_user")
    
    post = relationship('Post', back_populates='author', order_by="Post.created_at")
    comments = relationship('Comment', back_populates='author', order_by="Comment.created_at")
    admin_permissions = relationship('AdminPermission', back_populates='user', uselist=False)
    news = relationship('NewsItem', order_by="NewsItem.last_update", back_populates='recipient')
    reports = relationship('Report', back_populates='author')
    
    reposts = relationship("Post", primaryjoin="and_(User.id == Post.author_id, Post.is_reposted == True, Post.is_deleted == False)", overlaps="post,author")
    
    def __repr__(self):
        return f"User<id={self.id}, username={self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'picture': self.picture,
            'is_verified': self.is_verified,
        }
    
    def get_posts(self,  get_comments=False, get_deleted_posts=False):
        result = []
        posts = (
            db.session.query(Post).filter_by(author_id=self.id).order_by(
                case(
                    (Post.reposted_at != None, Post.reposted_at),
                    else_=Post.created_at
                )
            ).all())
        
        for post in posts:
            if not post.is_deleted or get_deleted_posts:
                is_liked = db.session.query(Like).filter_by(user_id=current_user.id, post_id=post.id).first()
                result.append({
                    'id': post.id,
                    'title': post.title,
                    'slug': post.slug,
                    'content': post.content,
                    'created_at': post.created_at.strftime("%Y/%m/%d %I:%M %p"),
                    'created_at_shorten': format_short_delta(datetime.now() - post.created_at) if post.created_at else None,
                    'is_edited': post.is_edited,
                    'edited_at': post.edited_at.strftime("%Y/%m/%d %I:%M %p") if post.edited_at else None,
                    'edited_at_shorten': format_short_delta(datetime.now() - post.edited_at) if post.edited_at else None,
                    'is_reposted': post.is_reposted,
                    'reference_id': post.reference if post.is_reposted else None,
                    'reference_username': db.session.get(Post, post.reference).author.username if post.is_reposted else None,
                    'reposted_at': post.reposted_at.strftime("%Y/%m/%d %I:%M %p") if post.is_reposted else None,
                    'reposted_at_shorten': format_short_delta(datetime.now() - post.reposted_at) if post.is_reposted else None,
                    'comments': post.get_comments() if get_comments else [],
                    'is_deleted': post.is_deleted if get_deleted_posts else None,
                    'deleted_at': post.deleted_at.strftime("%Y/%m/%d %I:%M %p") if get_deleted_posts and post.is_deleted else None,
                    'deleted_at_shorten': format_short_delta(datetime.now() - post.deleted_at) if get_deleted_posts and post.is_deleted else None,
                    'is_liked_by_current_user': bool(is_liked),
                    'likes_count': db.session.query(Like).filter_by(post_id=post.id).count(),
                    'is_reported': db.session.query(Report).filter_by(author_id=current_user.id, reference_table="posts", reference_id=post.id).first()
                })
        return result
    
    @property
    def likes(self):
        return db.session.query(Like).filter(Like.post_id.in_([el['id'] for el in self.get_posts()])).all()
    
    def mark_as_banned(self):
        self.is_banned = True
        self.banned_at = datetime.now()
            
        return self
    
    def mark_as_unbanned(self):
        self.is_banned = False
        self.banned_at = datetime.now()
            
        return self
    
    @property
    def received_comments(self):
        return (
            Comment.query
            .join(Comment.post)
            .filter(Post.author_id == self.id, Comment.is_deleted == False)
            .all()
        )
        
    @property
    def friends(self):
        friend_list = flatten(db.session.query(Friendship).filter(Friendship.user2_id == self.id).all()) + flatten(db.session.query(Friendship).filter(Friendship.user1_id == self.id).all())
        return [friend.user1_id if friend.user1_id != self.id else friend.user2_id for friend in friend_list]
        
    @property
    def reposted_posts(self):
        ref_post = aliased(Post)

        return (
            db.session.query(Post)
            .select_from(Post)
            .join(ref_post, Post.reference == ref_post.id)
            .filter(
                Post.is_deleted == False,
                Post.is_reposted == True,
                ref_post.author_id == self.id
            )
            .all()
        )
        
    @property
    def banned_at_shorten(self):
        return self.banned_at.strftime("%Y/%m/%d %I:%M %p")
        
    def find_updated_fields(self, form=None, files=None):
        potential_fields = {
            'username': { "name": self.username, "path": form },
            'picture': { "name": self.picture, "path": files }
        }
        
        fields_to_update = dict()
        for field in potential_fields:
            name = potential_fields[field]['name']
            path = potential_fields[field]['path'].get(field)
            
            if not(isinstance(path, FileStorage) and path.content_type == "application/octet-stream"):
                if name != path and path is not None:
                    fields_to_update.update({field: path})
        
        return fields_to_update
    
    def promote_admin(self):
        if self.admin_permissions:
            return
        
        new_admin = AdminPermission(id=self.id)
        db.session.add(new_admin)

        db.session.commit()
    
    def demote_admin(self):
        if not self.admin_permissions:
            return
        
        db.session.delete(self.admin_permissions[0])

        db.session.commit()