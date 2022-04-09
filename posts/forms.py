#!/usr/bin/python3
"""
Module auth
Handles Login, registration
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError, EqualTo, Email
from posts import User

class RegisterForm(FlaskForm):
	"""Registration form"""
	firstname = StringField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "First Name"})
	lastname = StringField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Last Name"})
	username = StringField(validators=[InputRequired(), Length(min=4,max=10, message="Please provide a valid name")], render_kw={"placeholder": "Username"})
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=6,max=20)], render_kw={"placeholder": "Password"})
	cpwd = PasswordField(validators=[InputRequired(), Length(8, 72),EqualTo("password", message="Passwords must match !")], render_kw={"placeholder": "Confirm Password"})
	submit = SubmitField("Register")

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("Email already registered!")

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).first():
			raise ValidationError("Username already taken!")

class LoginForm(FlaskForm):
	"""Login form"""
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
	remember = BooleanField('Remember Me',validators= [DataRequired()])
	submit = SubmitField("Login")