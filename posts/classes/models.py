#!/usr/bin/env python3

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base

from posts.helper_methods import _generate_uuid, _hash_password
from posts import login_user
Base = declarative_base()



@login_user.user_loader
def find_user(user):
    from posts.classes import storage
    return storage.get_user_by_id(user)


class User(Base, UserMixin):
    """User class inherits from declarative base"""
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    lpost = relationship('Lpost', backref='users', cascade='delete')

    def __init__(self, *args, **kwargs):
        """
        instantiates user object
        """
        self.email = ""
        self.password = ""

        for k, v in kwargs.items():
            if k is 'password':
                User.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password):
        """
            Encrypts password
        """
        secure_pw = _hash_password(password)
        setattr(self, 'password', secure_pw)

class Lpost(Base):
    """Lpost class inherits from declarative base"""
    __tablename__ = 'lpost'

    id = Column(Integer, primary_key=True)
    title = Column(String(12), nullable=False)
    ingridients = Column(Text, unique=True, nullable=False)
    recipe = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        """Initialize instance attributes"""
        self.title = ""
        self.ingridients = ""
        self.recipe = ""
        for k, v in kwargs.items():
            setattr(self, k, v)