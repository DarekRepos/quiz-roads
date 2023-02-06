
# from datetime import timedelta
# from flask_wtf import FlaskForm
# from flask import session, Flask
# from wtforms.csrf.session import SessionCSRF




# class MyBaseForm(FlaskForm):
#     class Meta:
#         csrf = True
#         csrf_class = SessionCSRF
#         #csrf_secret = app.config['CSRF_SECRET_KEY']
#         csrf_secret = b'EPj00jpfj8Gx1SjnyLxwBBSQfnQ9DJYe0Ym'
#         csrf_time_limit = timedelta(minutes=20)

#     @property
#     def csrf_context(self):
#         return session
