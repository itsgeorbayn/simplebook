from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
    
class InviteFriendForm(FlaskForm):
    username = StringField('Input user\'s name', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Send invite')