
from datetime import timedelta
from flask_wtf import FlaskForm
from flask import session, Flask
from wtforms.csrf.session import SessionCSRF

app = Flask(__name__)
#TODO: import secrete from env file 
class MyBaseForm(FlaskForm):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym'
        csrf_time_limit = timedelta(minutes=20)
    
    @property
    def csrf_context(self):
        return session
