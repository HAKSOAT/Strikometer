from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Submit")

class FeedbackForm(FlaskForm):
    upvote = SubmitField("Upvote")
    downvote = SubmitField("Downvote")
