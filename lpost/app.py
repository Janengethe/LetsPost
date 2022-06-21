#!/usr/bin/env python3
"""Module app"""
import os
from flask_login import login_required, login_user, current_user, LoginManager, logout_user
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for

from auth import Auth
from forms import logged_in, RegisterForm, LoginForm, PostForm

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please, Login to continue"

@login_manager.user_loader
def load_user(user_id):
    from db import User
    return User.query.get(int(user_id))

AUTH = Auth()

@app.route("/", methods=['GET'], strict_slashes=False)
def status() -> str:
    """Home"""
    form = PostForm()

    return render_template('index.html', form=form)

@app.route('/dashboard', methods=['POST', 'GET'], strict_slashes=False)
def dashboard():
    return render_template('dashboard.html')


@app.route('/user', methods=['POST', 'GET'], strict_slashes=False)
def register():
    """
    end-point to register a user
    Test on terminal:
        curl -XPOST localhost:5000/register -d
        'email=bob@me.com' -d 'password=mySuperPwd' -v
    """
    user_in = logged_in(current_user)
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            new_user = AUTH.register_user(email, password)
            
            if new_user is not None:
                # this_user = AUTH.valid_login(email, password)
                flash('Account created successfully!', 'success')
                session_id = AUTH.create_session(email)
                msg = {"email": email, "message": "logged in"}
                response = jsonify(msg)
                response.set_cookie("session_id", session_id)
                return redirect(url_for('dashboard'))
        except ValueError:
            flash('Email already registered!', 'error')
    return render_template('register.html', user_in=user_in, form=form)

@app.route('/session', methods=['POST', 'GET'], strict_slashes=False)
def login() -> str:
    """
    Login Route
    create a new session for the user, store it the session ID as a cookie
    with key "session_id" on the response and
    return a JSON payload of the form
    """
    form = LoginForm()
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False
    if form.validate_on_submit():
        user = AUTH.valid_login(email, password)
        if user:
            session_id = AUTH.create_session(email)
            # get_user = AUTH.get_user_from_session_id(session_id)
            msg = {"email": email, "message": "logged in"}
            response = jsonify(msg)
            response.set_cookie("session_id", session_id)
            print(response)
            login_user(current_user)
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password. Try again", "danger")
    return render_template('login.html', form=form, email=email, password=password, remember=remember)
	
@app.route('/session', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    The request is expected to contain the session ID as a cookie
    with key "session_id".
    Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    s_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(s_cookie)
    if s_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")