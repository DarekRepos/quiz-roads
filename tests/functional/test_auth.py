import flask
import pytest

from flask import session
from sqlalchemy import select

from quizproject.models.users import User


def test_login(client, auth, app_with_user):
    """
    GIVEN a Flask application configured for testing
          (test user are created with app_with_user)
    WHEN the '/login' page is requested (POST) with VALID data
    THEN check that the user can enter login page (page loaded - 200 status code)
         check that existing user is successfully login (status 200)
         check that user is successfully redirected to profile pageB
    """

    assert client.get("/auth/login").status_code == 200

    response = auth.login(email="dareczek014@gmail.com", password="dareczek014")

    assert response.status_code == 200
    assert response.request.path == "/profile"


def test_logout(client, auth, app_with_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the user is log in with VALID data
    THEN check that existing user is successfully login out
         check that there was one redirect response
         check that user is successfully redirected to index page
    """
    with client:
        # get index page
        client.get("/")

        # login to existing account
        auth.login("dareczek014@gmail.com", "dareczek014")

        # logout user
        response = auth.logout()

        # check user is successfuly loged out
        assert response.status_code == 200

        # Check that there was one redirect response.
        assert len(response.history) == 1

        # Check that the second request was to the index page.
        assert response.request.path == "/"

        # TODO: implement session
        # assert 'user_id' not in session


@pytest.mark.parametrize(
    ("username, email, password, confirm, message"),
    [
        (
            "dareczek046",
            "dareczek046@gmail.com",
            "dareczek046",
            "dareczek046",
            b"auth/login",
        ),
        (
            "dareczek014",
            "newdareczek014@gmail.com",
            "dareczek14",
            "dareczek014",
            b"already registered",
        ),
        (
            "newdareczek014",
            "dareczek014@gmail.com",
            "dareczek14",
            "dareczek014",
            b"already registered",
        ),
    ],
)
def test_register_validation(
    client, app_with_db, app_with_user, username, email, password, confirm, message
):
    """
    GIVEN a Flask application configured for testing and existing user in db
    WHEN login with valid data
    THEN check that existing user is successfully created (status code 200)

    """

    assert client.get("/auth/signup").status_code == 200
    response = client.post(
        "/auth/signup",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": confirm,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    ("username, email, password, confirm, redirection"),
    [
        (
            "dareczek046",
            "dareczek046@gmail.com",
            "dareczek046",
            "dareczek046",
            "/auth/login",
        ),
        (
            "dareczek014",
            "newdareczek014@gmail.com",
            "dareczek14",
            "dareczek014",
            "/auth/signup",
        ),
        (
            "newdareczek014",
            "dareczek014@gmail.com",
            "dareczek14",
            "dareczek014",
            "/auth/signup",
        ),
    ],
)
def test_register(
    client, app_with_db, app_with_user, username, email, password, confirm, redirection
):
    """
    GIVEN a Flask application configured for testing and existing user in db
    WHEN user register with valid data
         user register with existing email address
         user register with existing user name
    THEN check that the new user is successfully created with valid data
         check that user was redirect to page that he can change EMAIL
         check that user was redirect to page that he can change USERNAME
    """

    assert client.get("/auth/signup").status_code == 200
    response = client.post(
        "/auth/signup",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": confirm,
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert response.request.path == redirection
