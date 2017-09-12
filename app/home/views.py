from flask import render_template, flash, request
from flask.views import MethodView
from flask_login import current_user, login_required

from ..models import User
from . import home
from app.home.forms import ChangeEmailForm, ChangePasswordForm, ChangeUserDetailsForm

from app.utils.helper import register_view

"""
@home.route('/')
def homepage():
	return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
	return render_template('home/dashboard.html', title="Dashboard")
"""

class HomePage(MethodView):

	def get(self):
		return render_template('home/index.html', title="Welcome")

class UserProfile(MethodView):

	def get(self, username):
		user = User.query.filter_by(username=username).first_or_404()
		return render_template("home/user_profile.html", user=user)

class AllUserTopics(MethodView):

	def get(self, username):
		page = request.args.get("page", 1, type=int)
		user = User.query.filter_by(username=username).first_or_404()
		topics = user.all_topics(page, current_user)
		return render_template("home/all_topics.html", user=user, topics=topics)


class AllUserPosts(MethodView):

	def get(self, username):
		page = request.args.get("page", 1, type=int)
		user = User.query.filter_by(username=username).first_or_404()
		posts = user.all_posts(page, current_user)
		return render_template("home/all_posts.html", user=user, posts=posts)

class ChangePassword(MethodView):
	decorators = [login_required]
	form = ChangePasswordForm

	def get(self):
		return render_template("home/change_password.html", form=self.form())

	def post(self):
		form = self.form()
		if form.validate_on_submit():
			current_user.password = form.new_password.data
			current_user.save()

		flash("Password updated.", "success")
		return render_template("home/change_password.html", form=form)


class ChangeEmail(MethodView):
	decorators = [login_required]
	form = ChangeEmailForm

	def get(self):
		return render_template("home/change_email.html", form=self.form(current_user))

	def post(self):
		form = self.form(current_user)
		if form.validate_on_submit():
			current_user.email = form.new_email.data
			current_user.save()

		flash("Email address updated.", "success")
		return render_template("home/change_email.html", form=form)


class ChangeUserDetails(MethodView):
	decorators = [login_required]
	form = ChangeUserDetailsForm

	def get(self):
		return render_template("home/change_details.html", form=self.form(obh=current_user))

	def post(self):
		form = self.form(obj=current_user)

		if form.validate_on_submit():
			form.populate_obj(current_user)
			current_user.save()

		flash("User details updated.", "success")

		return render_template("home/change_details.html", form=form)


register_view(home, routes=['/'], view_func=HomePage.as_view('index'))

register_view(home, routes=['/setting/change_email'], view_func=ChangeEmail.as_view('change_email'))

register_view(home, routes=['/setting/change_password'], view_func=ChangePassword.as_view('change_password'))

register_view(home, routes=["/setting/change-details"], view_func=ChangeUserDetails.as_view('change_details'))

register_view(home, routes=['/<username>/posts'], view_func=AllUserPosts.as_view('view_all_posts'))

register_view(home, routes=['/<username>/topics'], view_func=AllUserTopics.as_view('view_all_topics'))

register_view(home, routes=['/<username>/profile'], view_func=UserProfile.as_view('profile'))

