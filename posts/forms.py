#!/usr/bin/env python3
"""Module forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from wtforms.validators import Email, ValidationError

from posts.database import storage


class RegisterForm(FlaskForm):
    """Registration form"""
    email = StringField(
        validators=[InputRequired(), Email(), Length(1, 64)],
        render_kw={"placeholder": "Email"})
    password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20), EqualTo(
            "password", message="Passwords must match!")],
        render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Sign Up")

    def validate_email(self, email: str) -> None:
        """Validate email"""
        user = storage.get_user_by_email(email.data)
        if user:
            raise ValidationError('Email already taken')
        return


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField(
        validators=[InputRequired(), Email(), Length(1, 64)],
        render_kw={"placeholder": "Email"})
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


class PostForm(FlaskForm):
    """Post form"""
    post = StringField('Title', validators=[DataRequired(), Length(min=4)])
    ingridients = StringField(
        'Ingridients', validators=[DataRequired(), Length(min=4)])
    recipe = StringField('Recipe', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Post')
