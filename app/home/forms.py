from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, ValidationError, SubmitField
from wtforms.validators import Length, DataRequired, InputRequired, Email, EqualTo, Optional, URL

from app import db
#from .models import User

"""
class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Password', 
		validators=[DataRequired(message="Please enter your password.")])

	new_password = PasswordField('New password', 
		validators=[InputRequired(), EqualTo('confirm_new_password', message="New passwords must match.")])

	confirm_new_password = PasswordField("Confirm new password")

	submit = SubmitField("Save")

	def validate_old_password(self, field):
		if not current_user.check_password(field.data):
			raise ValidationError("Old password is wrong.")

class ChangeEmailForm(FlaskForm):
	old_email = StringField('Old email', 
		validators=[DataRequired("A valid email address is required."), Email("Invalid email address.")])

	new_email = StringField('New email', 
		validators=[InputRequired(), EqualTo('confirm_new_email', message="Email addresses must match."),
		Email("Invalid email address.")])

	confirm_new_email = StringField("Confirm email address", 
		validators=[Email("Invalid email address.")])

	submit = SubmitField("Save")

	def __init__(self, user, *args, **kwargs):
		self.user = user
		kwargs['obj'] = self.user
		super(ChangeEmailForm, self).__init__(*args, **kwargs)

	def validate_email(self, field):
		user = User.query.filter(db.and_(
		User.email.like(field.data),
		db.not_(User.id == self.user.id))).first()
		if user:
			raise ValidationError("This email address is already taken.")


class ChangeUserDetailsForm(FlaskForm):

	location = StringField('Location', validators=[Optional()])
	occupation = StringField('Occupation', validators=[Optional()])
	organization = StringField('Organization', validators=[Optional()])
	bio = TextAreaField('Bio', validators=[Optional(), Length(min=0, max=5000)])

	github = StringField('Github', validators=[Optional()])
	kaggle = StringField('Kaggle', validators=[Optional()])
	linkedin = StringField('LinkedIn', validators=[Optional(), URL()])

	avatar = StringField('Avatar', validators=[Optional(), URL()])

	submit = SubmitField('Save')

"""
