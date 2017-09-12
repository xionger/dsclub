from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

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

