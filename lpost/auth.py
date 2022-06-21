#!/usr/bin/env python3
"""
Module auth
"""
from typing import Union
import bcrypt
from db import DB, User
import uuid
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    returned bytes is a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def _generate_uuid() -> str:
    """return a string representation of a new UUID."""
    return str(uuid.uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialization"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register_user takes mandatory email and password arguments
        and return a User object.
        If a user already exist with the passed email, raises a ValueError.
        If not, hashes the password with _hash_password, save the user to the
        database using self._db and returns the User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hpassword = _hash_password(password)
            user = self._db.add_user(email, hpassword)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True. In any other case, return False
        """
        try:
            user = self._db.find_user_by(email=email)
            return(bcrypt.checkpw(
                password.encode("utf-8"), user.password))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        finds the user corresponding to the email,
        generate a new UUID and store it in the database as
        the user’s session_id, then return the session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
        If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session
        updates the corresponding user’s session ID to None
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
