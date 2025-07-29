from app.extensions import db
from sqlalchemy.orm import relationship
from datetime import datetime
from app.utils import translate_checkbox

class AdminPermission(db.Model):
    __tablename__ = 'admin_permissions'
    
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    list_users = db.Column(db.Boolean, default=True)
    edit_users = db.Column(db.Boolean, default=False)
    ban_users = db.Column(db.Boolean, default=False)
    
    list_admins = db.Column(db.Boolean, default=True)
    edit_admins = db.Column(db.Boolean, default=False)
    
    list_posts = db.Column(db.Boolean, default=True)
    edit_posts = db.Column(db.Boolean, default=False)
    remove_posts = db.Column(db.Boolean, default=False)
    
    list_comments = db.Column(db.Boolean, default=True)
    edit_comments = db.Column(db.Boolean, default=False)
    remove_comments = db.Column(db.Boolean, default=False)
    
    list_messages = db.Column(db.Boolean, default=True)
    edit_messages = db.Column(db.Boolean, default=False)
    remove_messages = db.Column(db.Boolean, default=False)
    
    list_reports = db.Column(db.Boolean, default=True)
    close_reports = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_edited = db.Column(db.DateTime, default=datetime.now())
    
    user = relationship('User', back_populates='admin_permissions')
    
    def actions(self):
        potential_actions = {
            'Show users': {'name': 'list_users', 'allow': self.list_users},
            'Show posts': {'name': 'list_posts', 'allow': self.list_posts, },
            'Show messages': {'name': 'list_messages', 'allow': self.list_messages, },
            'Show admins': {'name': 'list_admins', 'allow': self.list_admins, },
            'Moderate panel': {'name': 'list_reports', 'allow': self.list_reports, },
        }
        
        return {
            label: info
            for label, info in potential_actions.items()
            if info['allow']
        }
        
    def find_updated_fields(self, form):
        potential_fields = {
            'list_users': self.list_users,
            'edit_users': self.edit_users,
            'ban_users': self.ban_users,
            'list_admins': self.list_admins,
            'edit_admins': self.edit_admins,
            'list_posts': self.list_posts,
            'edit_posts': self.edit_posts,
            'remove_posts': self.remove_posts,
            'list_comments': self.list_comments,
            'edit_comments': self.edit_comments,
            'remove_comments': self.remove_comments,
            'list_messages': self.list_messages,
            'edit_messages': self.edit_messages,
            'remove_messages': self.remove_messages,
            'list_reports': self.list_reports,
            'close_reports': self.close_reports,
        }
        
        fields_to_update = dict()
        for field in potential_fields:
            this_field = translate_checkbox(form.get("admin_permission_" + field))
            if potential_fields[field] != this_field:
                fields_to_update.update({field: this_field})

        return fields_to_update    
    
    @property
    def created_at_shorten(self):
        return self.created_at.strftime("%Y/%m/%d %I:%M %p")

    @property
    def last_edited_shorten(self):
        return self.last_edited.strftime("%Y/%m/%d %I:%M %p")