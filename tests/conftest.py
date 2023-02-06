from flask import Flask
import pytest

from config import TestingConfig

# import the module
from quizproject import create_app, db


@pytest.fixture()
def app():
    app = Flask(__name__)

    app = create_app(TestingConfig)

    app.config.update({
        "TESTING": True,
        "SECRET_KEY": 'test',
    })

    with app.app_context():
        db.create_all()

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, email='dareczek011@gmail.com', password='dareczek011'):
        return self._client.post(
            '/login',
            data={'email': email, 'password': password},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/logout',  follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)
