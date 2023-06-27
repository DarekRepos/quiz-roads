import datetime
import scrypt

from flask import (
    render_template,
    redirect,
    session,
    url_for,
    request,
    current_app,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from config import Config

from quizproject.tasks.tasks import send_celery_email
from .. import db
from ..models.users import User
from .forms import LoginForm, SignUpForm
from . import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    form = LoginForm(request.form)

    remember = bool(form.remember_me.data)

    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        # check if the user actually exists
        # take the user-supplied password, hash it,
        # and compare it to the hashed password in the database

        # Verify the hashed password
        is_password_valid = (
            scrypt.hash(
                form.password.data.encode("utf-8"),
                salt=Config.SALT,
                N=2048,
                r=8,
                p=1,
                buflen=32,
            )
            == user.user_password
        )

        if not user or not is_password_valid:
            flash("Please check your login details and try again.")
            return render_template("auth/login.html", form=form)

        # if the above check passes,
        # then we know the user has the right credentials
        login_user(user, remember=remember)

        current_app.logger.info(f"User login : {str(user)}")

        message_data = {
            "subject": "Hello app!",
            "body": "Thank you for the register.",
            "recipients": user.user_email,
        }
        send_celery_email.apply_async(args=[message_data])

        return redirect(url_for("main.profile"))

    if not current_user.is_authenticated:
        return render_template("auth/login.html", form=form)

    return render_template("auth/login.html", form=form)


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    """_summary_

    Returns:
        _type_: _description_
    """
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        # TODO: validate errors save to logs
        register_time = datetime.datetime.utcnow()

        # Check if email exists
        user = User.query.filter_by(user_email=form.email.data).first()

        if user:
            flash("Email address already registered")
            return redirect(url_for("auth.signup"))

        # check if user exists
        user = User.query.filter_by(user_name=form.username.data).first()

        if user:
            flash("username address already registered")
            return redirect(url_for("auth.signup"))

        # Create new User from form data

        new_user = User(
            user_email=form.email.data,
            user_name=form.username.data,
            user_password=scrypt.hash(
                form.password.data.encode("utf-8"),
                salt=Config.SALT,
                N=2048,
                r=8,
                p=1,
                buflen=32,
            ),
            register_time=register_time,
        )

        current_app.logger.info(f"Create new user  {str(user)}")

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info(f"Added user to the database: {str(new_user)}")

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """
    Log out the user and redirect to index page

    Returns:
        url: index page
    """
    logout_user()
    session.clear()
    return redirect(url_for("main.index"))
