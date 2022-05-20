#!/usr/bin/python3
"""
Module routes
Contains the routes
"""
from posts import app, User, db
from flask import jsonify
from posts.helpers import logged_in
from posts.forms import LoginForm, RegisterForm
from flask import render_template, url_for, redirect, flash, request
from posts.forms import RegisterForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, login_required, logout_user, current_user
import requests


bcrypt = Bcrypt(app)

@app.route("/", strict_slashes=False)
def index():
	"""Index route"""
	return render_template('index.html')

@app.route('/dashboard', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/register', methods=['POST', 'GET'], strict_slashes=False)
def register():
	"""Returns landing page in response to registration"""
	user_in = logged_in(current_user)
	form = RegisterForm()
	if form.validate_on_submit():
		first = form.firstname.data
		last = form.lastname.data
		user = form.username.data
		email = form.email.data
		h_psswd = bcrypt.generate_password_hash(form.password.data)
		new_user = User(firstname=first, lastname=last, username=user, email=email, password=h_psswd)

		db.session.add(new_user)
		db.session.commit()
		flash('A warm welcome!', 'success')
		login_user(new_user)
		return redirect(url_for('dashboard'))

	return render_template('register.html', user_in=user_in, form=form)

@app.route('/login', methods=['POST', 'GET'], strict_slashes=False)
def login():
	"""Return home page upon login"""
	form = LoginForm()
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			return redirect(url_for('dashboard'))
		else:
			flash("Invalid email or password", "danger")
	return render_template('login.html', form=form, email=email, password=password, remember=remember)

@app.route('/logout', methods=['POST', 'GET'], strict_slashes=False)
@login_required
def logout():
    logout_user()
    flash("See you later!", "success")
    return redirect(url_for('index'))
