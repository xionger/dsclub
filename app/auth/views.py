from flask import flash, redirect, render_template, url_for, request
from flask import current_app as app
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

from app.utils.helper import redirect_or_next, register_view
from app.utils.exceptions import AuthenticationError

class Register(MethodView):

    def form(self):
        form = RegistrationForm()
        form.process(request.form)  # needed because a default is overriden
        return form

    def get(self):
        return render_template("auth/register.html", form=self.form(), title='Register')

    def post(self):
        form = self.form()

        if form.validate_on_submit():
            user = form.save()

            # redirect to the login page
            return redirect(url_for('home.index'))

        return render_template("auth/register.html", form=form, title='Register')

class Login(MethodView):

    def form(self):
        form = LoginForm()
        return form

    def get(self):
        return render_template("auth/login.html", form=self.form())

    def post(self):
        form = self.form()
        if form.validate_on_submit():

            try:
                user = User.authenticate(form.username.data, form.password.data)

                if not login_user(user, remember=form.remember_me.data):
                    flash("Please activate your account", "danger")

                return redirect(url_for("home.index"))

            except AuthenticationError:
                flash("Wrong username or password.", "danger")

        return render_template("auth/login.html", form=form)

class Logout(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        flash("Logged out", "success")

        return redirect(url_for("home.index"))


register_view(auth, routes=['/register'], view_func=Register.as_view('register'))
register_view(auth, routes=['/login'], view_func=Login.as_view('login'))
register_view(auth, routes=['/logout'], view_func=Logout.as_view('logout'))

"""
@auth.route('/register', methods=['GET', 'POST'])
def register():

    #Handle requests to the /register route
    #Add a user to the database through the registration form

    form = RegistrationForm()
    if form.validate_on_submit():
        """"""
        user = User(email=form.email.data.lower(),
                    username=form.username.data.lower(),
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    password=form.password.data)

        # add the user to the database
        db.session.add(user)
        db.session.commit()
        """"""
        user = form.save()

        flash('You have successfully registered! Please login now.')

        # redirect to the login page
        return redirect(url_for('home.dashboard'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():

    #Handle requests to the /login route
    #Log a user in through the login form

    form = LoginForm()
    if form.validate_on_submit():

        # check whether the user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))

        # when login details are incorrect
        else:
            flash('Invalid email or password.')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():

    #Handle requests to the /logout route
    #Log a user out through the logout link

    logout_user()
    flash('You have successfully logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/logout/<user_id>')
@login_required
def update_profile(user_id):
    
    return render_template('auth/update_profile.html')

"""

