from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    sender = StringField('Your Name')
    reach_at = StringField('Email or Phone Number')


class PostForm(FlaskForm):
    title = StringField('Title or Subject', validators=[DataRequired(), Length(max=80, message="Please use a shorter title")])
    body = TextAreaField('Post', validators=[DataRequired()])