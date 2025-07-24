from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from .validators import HasNoSpecialChar

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4), HasNoSpecialChar('@')])
    email = EmailField('Email', validators=[DataRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    agree = BooleanField('Agree with company\'s terms of service', validators=[DataRequired()])
    submit = SubmitField('Register')
    