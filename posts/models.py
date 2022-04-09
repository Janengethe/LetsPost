#!/usr/bin/python3
"""
Module models
classes
"""
# from posts import app
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from wtforms.validators import ValidationError


# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(12), nullable=False)
#     lastname = db.Column(db.String(12), nullable=False)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)

# def validate_username(self, username):
# 	"""
# 	Method to validate an existing user
# 	"""
# 	existing = User.query.filter_by(username.username.data).all()
# 	if existing:
# 		raise ValidationError("Username already exists")