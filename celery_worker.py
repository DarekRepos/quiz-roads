#!/usr/bin/env python
import os

# from app import create_app, celery
from quizproject import create_app

app = create_app()
app.app_context().push()

from quizproject import celery
