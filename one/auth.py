#!/usr/bin/env python3
"""
Module auth
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    returned bytes is a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialization"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hpassword = _hash_password(password)
            user = self._db.add_user(email, hpassword)
            return user
