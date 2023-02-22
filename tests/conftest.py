import datetime
import pytest
from sqlalchemy import delete

from config import TestingConfig

# import the module
from quizproject import create_app
from quizproject import db as _db
from models.users import User

from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():
    """
    Returns session-wide application.
    """

    app = create_app(TestingConfig)

    app.config.update({
        "TESTING": True,
        "SECRET_KEY": 'test',
    })

    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture(scope="session")
async def app_with_db(app):
    _db.create_all()

    yield app

    _db.session.commit()
    _db.drop_all()


@pytest.fixture()
def app_with_user(app_with_db):
    register_time = datetime.datetime.utcnow()
    new_user = User(register_time=register_time,
                    user_email="dareczek014@gmail.com",
                    user_password=generate_password_hash(
                                  'dareczek014',
                                  method='sha256'),
                    user_name='dareczek014')

    # add the new user to the database
    _db.session.add(new_user)
    _db.session.commit()

    yield app_with_db
    _db.session.execute(delete(User))
    _db.session.commit()
    _db.session.remove()


@pytest.fixture()
def client(app, app_with_db):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):

    def __init__(self, client):
        self._client = client

    def login(self, email, password):
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
