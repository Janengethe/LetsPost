#!/usr/bin/python3
"""
__init__ module
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from wtforms.validators import ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'uIZue4SCjF2UBgooqv+Dl8v+4IGqnd'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please, Sign up first"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = "user"

	id = db.Column(db.Integer, primary_key=True)
	firstname = db.Column(db.String(12), nullable=False)
	lastname = db.Column(db.String(12), nullable=False)
	username = db.Column(db.String(20), nullable=False, unique=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False, unique=True)

	lpost = db.relationship('Lpost', backref='user')

	# def __init__(self, firstname, lastname, username, email, password):
	# 	self.firstname = firstname
	# 	self.lastname = lastname
	# 	self.username = username
	# 	self.email = email
	# 	self.password = bcrypt.generate_password_hash(password).decode('utf-8')

	def __repr__(self):
		return '<User %r>' % self.username
		# return ("User: {} Password: {}".format(self.email, self.password))

def validate_username(self, username):
	"""
	Method to validate an existing user
	"""
	if User.query.filter_by(username.username.data).all():	
		raise ValidationError("Username already in use.")


class Lpost(db.Model, UserMixin):
	__tablename__ = 'lpost'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(12), nullable=False)
	content = db.Column(db.Text)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


from posts import routes