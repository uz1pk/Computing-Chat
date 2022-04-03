from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User

# Function to validate user crendentials when logging in
def valid_user_data(form, field):
    current_username = form.username.data
    current_password = field.data

    current_user = User.query.filter_by(username = current_username).first()
    if current_user is None:
        raise ValidationError("Login credentials are not correct")
    elif current_password != current_user.password:
        raise ValidationError("Login credentials are not correct")

# Function to see if the account already exists
def validate_registration(form, field): 
    current_username = field.data

    current_user = User.query.filter_by(username = current_username).first()
    if current_user:
        raise ValidationError("Username already exists")

# Registration form
class RegistrationForm(FlaskForm): # Registration form
    username = StringField('username_label',
    validators=[InputRequired(message="Must Enter Username"), Length(min=4, max=25, message="Username must be greater than 4 characters"), validate_registration])

    password = PasswordField('password_label', 
    validators=[InputRequired(message="Must Enter Password"), Length(min=5, message="Password must be greater than 4 characters")])

    confirm_password = PasswordField('confirm_password_label', 
    validators=[InputRequired(message="Must Enter Username"), EqualTo('password', message="Passwords must match")]) #all validators for each field

    submit_button = SubmitField('Create')


# Login form
class UserLoginForm(FlaskForm):
    username = StringField('username_label', validators=[InputRequired(message="Must Enter Username")])
    password = PasswordField('password_label', validators=[InputRequired(message="Must Enter Password"), valid_user_data])
    submit_button = SubmitField('Login')

