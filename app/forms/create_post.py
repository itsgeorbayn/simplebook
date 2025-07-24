from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed

from wtforms.validators import DataRequired, Length
    
class CreatePostForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=8, max=64)], render_kw={"placeholder": "Input your thoughts there..."})
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create Post')