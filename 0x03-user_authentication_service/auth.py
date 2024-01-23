#!/usr/bin/env python3
"""User authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt"""
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed


def _generate_uuid() -> str:
    """generate and return uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashedpwd = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashedpwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login"""
        try:
            user = self._db.find_user_by(email=email)
            hashedpw = user.hashed_password
            encode = password.encode("utf-8")
            return bcrypt.checkpw(encode, hashedpw)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """create session id"""
        try:
            user = self._db.find_user_by(email=email)
            id = user.id
            session_id = _generate_uuid()
            self._db.update_user(id, session_id=session_id)
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> User:
        """get user from sesion id"""
        if not session_id:
            return
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return

    def destroy_session(self, user_id: str) -> None:
        """clear a users session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return
        except NoResultFound or ValueError:
            return
