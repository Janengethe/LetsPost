#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo, Email, ValidationError

from posts.classes import storage

class RegisterForm(FlaskForm):
	"""Registration form"""
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=6,max=20)], render_kw={"placeholder": "Password"})
	confirm_password = PasswordField(validators=[InputRequired(), Length(min=6,max=20),EqualTo("password", message="Passwords must match!")], render_kw={"placeholder": "Confirm Password"})
	submit = SubmitField("Sign Up")

	def validate_email(self, email):
		user = storage.get_user_by_email(email.data)
		if user:
			raise ValidationError('Email already taken')
		return

	
class LoginForm(FlaskForm):
	"""Login form"""
	email = StringField(validators=[InputRequired(), Email(), Length(1, 64)], render_kw={"placeholder": "Email"})
	password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
	remember = BooleanField('Remember Me',validators= [DataRequired()])
	submit = SubmitField("Login")


class PostForm(FlaskForm):
	"""Post form"""
	title = StringField(validators=[InputRequired(), Length(1, 12)], render_kw={"placeholder": "Title"})
	ingridients = StringField(validators=[InputRequired(), Length(1, 12)], render_kw={"placeholder": "Upload"})
	recipe = StringField(validators=[InputRequired()], render_kw={"placeholder": "Recipe"})
	submit = SubmitField('Post')