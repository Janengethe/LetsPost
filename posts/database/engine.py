#!/usr/bin/env python3
"""Module engine"""

from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text

Base = declarative_base()


class User(Base, UserMixin):
    """
    User class inherits from declarative base
    """
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    posts = relationship('Post', backref='users', cascade='delete')

    def __init__(self, *args, **kwargs) -> None:
        """
        instantiates user object
        """
        self.email = ""
        self.password = ""

        for k, v in kwargs.items():
            if k == 'password':
                User.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password: str) -> None:
        """
            Encrypts password
        """
        secure_pw = generate_password_hash(password)
        setattr(self, 'password', secure_pw)


class Post(Base):
    """Post class inherits from declarative base"""
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    post = Column(String(12), nullable=False)
    ingridients = Column(Text, nullable=False)
    recipe = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs) -> None:
        """
        Initialize instance attributes
        """
        self.post = ""
        self.ingridients = ""
        self.recipe = ""
        for k, v in kwargs.items():
            setattr(self, k, v)


class DBStorage():
    """Class for database storage"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initialization"""
        self.__engine = create_engine('sqlite:///ldb.db')
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def save(self, obj: dict) -> None:
        """
           create new obj and save entry to db
        """
        try:
            self.__session.add(obj)
            self.__session.commit()
        except ValueError:
            self.__session.rollback()

    def delete(self, obj: dict) -> None:
        """
           delete obj from db
        """
        self.__session.delete(obj)
        self.__session.commit()
        self.__session.flush()

    def all(self) -> dict:
        """Returns all items from the database"""
        post_dic = {}
        for obj in self.__session.query(Post).all():
            key = obj.id
            post_dic[key] = obj
        return post_dic

    def count(self) -> int:
        """
           count posts
        """
        total = 0
        for _ in self.__session.query(Post).all():
            total += 1
        return total

    def get_post_by_id(self, post_id: int) -> Post:
        """
           return post if username given
        """
        try:
            obj = self.__session.query(Post).filter_by(id=post_id).first()
            return obj
        except (IndexError, TypeError):
            return None

    def get_post_by_user(self, user_id: int) -> Post:
        """
            return post associated with user
        """
        try:
            obj = self.__session.query(Post).filter_by(user_id=user_id).all()
            return obj
        except (IndexError, TypeError):
            return None

    def get_user_by_email(self, email: str) -> User:
        """
            return user info
        """
        try:
            obj = self.__session.query(User).filter_by(email=email).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_email X____X')
            return None

    def get_user_by_id(self, user_id: int) -> User:
        """
            return user info
        """
        try:
            obj = self.__session.query(User).filter_by(id=user_id).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_id X____X')
            return None

    def reload(self) -> None:
        """
           creates all tables in database & session from engine
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self) -> None:
        """
            calls remove() on private session attribute (self.session)
        """
        self.__session.remove()
