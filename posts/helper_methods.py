#!/usr/bin/env python3
"""Module helper_methods"""
import bcrypt
import uuid


def _hash_password(password: str) -> bytes:
    """
    returned bytes is a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_passwd_b(password: str) -> bool:
    return bcrypt.checkpw(password, _hash_password(password))


def _generate_uuid() -> str:
    """return a string representation of a new UUID."""
    return str(uuid.uuid4())


def logged_in(current_user: int) -> bool:
    """returns True if user is logged in"""
    try:
        _ = current_user.id
        return True
    except ValueError:
        return False
