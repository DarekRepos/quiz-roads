from flask import Flask
import pytest

from config import TestingConfig

# import the module
from quizproject import create_app, db


@pytest.fixture()
def app():

    app = create_app(TestingConfig)

    app.config.update({
        "TESTING": True,
        "SECRET_KEY": 'test',
        "CSRF_SECRET_KEY": 'testing',
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