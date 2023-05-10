import datetime


from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models.users import User
from flask_login import login_user, login_required, logout_user, current_user
from . import db

from .forms.login_form import LoginForm
from .forms.signup_form import SignUpForm


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm(request.form)

    remember = True if form.remember_me.data else False

    # TODO: implement session
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it,
        # and compare it to the hashed password in the database
        if not user or not check_password_hash(
                user.user_password, form.password.data):

            flash('Please check your login details and try again.')
            return render_template('login.html', form=form)
        # if the above check passes,
        # then we know the user has the right credentials
        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))

    if not current_user.is_authenticated:
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        # TODO: validate errors save to logs
        register_time = datetime.datetime.utcnow()

        # Check if email exists
        user = User.query.filter_by(user_email=form.email.data).first()

        if user:
            flash('Email address already registered')
            return redirect(url_for('auth.signup'))

        # check if user exists
        user = User.query.filter_by(user_name=form.username.data).first()

        if user:
            flash('username address already registered')
            return redirect(url_for('auth.signup'))

        # Create new User from form data
        new_user = User(user_email=form.email.data,
                        user_name=form.username.data,
                        user_password=generate_password_hash(
                            form.password.data,
                            method='sha256'),
                        register_time=register_time)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
