from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
    
class VerificationForm(FlaskForm):
    verification_code = StringField('Verification code', validators=[DataRequired(), Length(min=6, max=6, message="Length must be exactly 6 characters")])
    submit = SubmitField('Verificate')