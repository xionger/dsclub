from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email, EqualTo, regexp, ValidationError

from app.models import User
from .. import db

USERNAME_RE = r'^[\w.+]+$'
is_valid_username = regexp(USERNAME_RE, message="You can only use letters or numbers.")

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20


class RegistrationForm(FlaskForm):

    #Form for users to create new account

    email = StringField('Email', 
        validators=[DataRequired("A valid email address is required."), Email("Invalid email address.")])

    username = StringField('Username', 
        validators=[DataRequired("A valid username is required."), is_valid_username])

    password = PasswordField('Password', 
        validators=[DataRequired("Please enter your password."), 
        EqualTo('confirm', message='Password must match')])

    confirm = PasswordField('Repeat Password')

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username is already in use.')

        if len(field.data) < USERNAME_MIN_LENGTH or len(field.data) > USERNAME_MAX_LENGTH:
            raise ValidationError(_(
                "Username must be between %(min)s and %(max)s characters long.",
                min=USERNAME_MIN_LENGTH, max=USERNAME_MAX_LENGTH)
            )


    def save(self):
        #with app.app_context():
        user = User(username=self.username.data.lower(), 
            email=self.email.data.lower(),
            password=self.password.data,
            date_joined=datetime.utcnow())

        return user.save()


class LoginForm(FlaskForm):

    #Form for users to login
    username = StringField('Username', validators=[DataRequired("Please enter your username.")])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])

    remember_me = BooleanField('Remember me', default=False)

    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email address', 
        validators=[DataRequired("A valid email address is required."), Email()]) 

    submit = SubmitField("Request Password")

class ResetPasswordForm(FlaskForm):
    token = HiddenField('Token')

    email = StringField('Email address', 
        validators=[DataRequired("A valid email address is required."), Email()])

    password = PasswordField('Password', 
        validators=[InputRequired(), EqualTo('confirm_password', message='Passwords must match.')])

    confirm_password = PasswordField('Confirm password')

    submit = SubmitField("Reset password")

    def validate_email(self, field):
        email = User.query.filter_by(email=field.data.lower()).first()
        if not email:
            raise ValidationError("Wrong email address.")