import datetime
from flask import Blueprint, render_template,redirect,url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from . import db

from .forms.loginform import LoginForm
from .forms.signupform import SignUpForm


auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET'])
# def login():
#     form = LoginForm(request.form)
#     return render_template('login.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
 
    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.user_password, password):
            flash('Please check your login details and try again.')
        
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)

        return redirect(url_for('main.profile'))
        
    return render_template('login.html', form=form)

# @auth.route('/signup')
# def signup():
#     return render_template('signup.html')

@auth.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
            
        register_time = datetime.datetime.utcnow()

        user = User.query.filter_by(user_email=email).first() 

        if user: 
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(user_email=email, user_name=name, user_password=generate_password_hash(password, method='sha256'),register_time=register_time)

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
