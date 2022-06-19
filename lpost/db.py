#!/usr/bin/env python3
"""
Module user
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


Base = declarative_base()


class User(Base):
    """User class inherits from declarative base"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))

    lpost = relationship('Lpost', backref='users')

    def __repr__(self):
        return f"User(id={self.id!r})"


class Lpost(Base):
    """Lpost class inherits from declarative base"""
    __tablename__ = 'lpost'

    id = Column(Integer, primary_key=True)
    title = Column(String(12), nullable=False)
    photo = Column(Text, unique=True, nullable=False)
    recipe = Column(Text, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///ldb.db")
        # Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        DB._session is a private property and hence
        should NEVER be used from outside the DB class.
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, password: str) -> User:
        """
        Saves the user to the db
        """
        user = User(email=email, password=password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        takes in arbitrary keyword arguments and
        returns the first row found in the users table as
        filtered by the method’s input arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except AttributeError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update the user’s attributes as passed in the method’s
        arguments then commit changes to the database.
        """
        user = self.find_user_by(id=user_id)

        for k, v in kwargs.items():
            if hasattr(user, k):
                setattr(user, k, v)
            else:
                raise ValueError
        self._session.commit()
        return None
