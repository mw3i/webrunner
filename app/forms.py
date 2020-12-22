# external 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional

# internal
# from app.models import User

class ConsentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    consent = BooleanField('I consent to participate in the experiment.', validators=[DataRequired()])
    submit = SubmitField('Start')

class DebriefForm(FlaskForm):
    Q1 = StringField('Question 1', validators=[Optional()])
    Q2 = BooleanField('Question 2', validators=[Optional()])
    submit = SubmitField('Submit Survey and Receive Credit')

