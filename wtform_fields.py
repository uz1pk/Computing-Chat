from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    """ Registration form """

    username = StringField('username_label',
     validators=[InputRequired(message="Must Enter Username"), Length(min=4, max=25, message="Username must be greater than 4 characters")])

    password = PasswordField('password_label', 
    validators=[InputRequired(message="Must Enter Password"), Length(min=4, max=25, message="Password must be greater than 4 characters")])

    confirm_password = PasswordField('confirm_password_label', 
    validators=[InputRequired(message="Must Enter Username"), EqualTo('password', message="Passwords must match")]) #all validators for each field

    submit_button = SubmitField('Create')
