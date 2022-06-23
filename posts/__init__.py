#!/usr/bin/env python3
"""Module app"""
import os
from flask_login import LoginManager
from flask import Flask


SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_user = LoginManager(app)
login_user.login_view = 'login'
login_user.login_message = 'Please, Login to continue'


@login_user.user_loader
def find_user(user):
    from posts.database import storage
    return storage.get_user_by_id(user)


from posts import routes