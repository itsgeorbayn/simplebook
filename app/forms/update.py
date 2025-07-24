from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo
from .validators import HasNoSpecialChar

class UpdateForm(FlaskForm):
    username = StringField('Username')
    new_password = PasswordField('New password')
    confirm_new_password = PasswordField('Confirm new password')
    picture = FileField('Picture')
    
    def __init__(self, field=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_field = field
        
        if field == "username":
            self.username.validators = [Length(min=4), DataRequired()]
        elif field == "picture":
            self.picture.validators = [FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'You can upload only pictures!'), DataRequired()]
        elif field == "password":
            self.new_password.validators = [DataRequired(), Length(min=6)]
            self.confirm_new_password.validators = [DataRequired(), Length(min=6), EqualTo('new_password', message='Passwords must match!')]
            
    old_password = PasswordField('Password', validators=[DataRequired()])