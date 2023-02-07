import pytest
from flask import g, session, url_for
from quizproject import engine


def test_login(client, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (POST) with VALID data
    THEN check that thge user can enter login page (page loaded - 200 status code)
         check that existing user is successfully login
         check that user is successfully redirected to profile page
    """

    assert client.get('/login').status_code == 200
    response = auth.login()
    assert response.status_code == 200

    assert response.request.path == '/profile'

    with client:
        client.get('/')

        # TODO: implement session
        # assert session['user_id'] == 1
        # assert g.user['username'] == 'dareczek011@gmail.com'


def test_logout(client, auth):
    """
    GIVEN a Flask application configured for testing
    WHEN the user is log in with VALID data
    THEN check that existing user is successfully login out
         check that there was one redirect response
         check that user is successfully redirected to index page
    """
    with client:
        # get index page
        client.get('/')

        auth.login()

        response = auth.logout()
        # check user is successfuly loged out
        assert response.status_code == 200

        # Check that there was one redirect response.
        assert len(response.history) == 1
        # Check that the second request was to the index page.
        assert response.request.path == "/"

        # TODO: implement session
        # assert 'user_id' not in session
