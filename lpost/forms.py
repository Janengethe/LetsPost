#!/usr/bin/python3
"""
Module auth
Handles Login, registration
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, ValidationError, EqualTo, Email

from db import User

def logged_in(current_user):
	"""returns True if user is logged in"""
	try:
		_ = current_user.id
		return True
	except:
		return False

class RegisterForm(FlaskForm):
	"""Registration form"""
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=6,max=20)], render_kw={"placeholder": "Password"})
	cpwd = PasswordField(validators=[InputRequired(), Length(min=6,max=20),EqualTo("password", message="Passwords must match!")], render_kw={"placeholder": "Confirm Password"})
	submit = SubmitField("Register")

	# def validate_email(self, email):
	# 	if User.query.filter_by(email=email.data).first():
	# 		raise ValidationError("Email already registered!")

	
class LoginForm(FlaskForm):
	"""Login form"""
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
	remember = BooleanField('Remember Me',validators= [DataRequired()])
	submit = SubmitField("Login")