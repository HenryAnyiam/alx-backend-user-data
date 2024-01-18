#!/usr/bin/env python3
"""Module to handle Session Based Authentication"""

from uuid import uuid4
from api.v1.auth.auth import Auth
from models.user import User
from models.base import DATA


class SessionAuth(Auth):
    """handle session based authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates session ID"""
        if not user_id or not isinstance(user_id, str):
            return None
        key_id = str(uuid4())
        type(self).user_id_by_session_id[key_id] = user_id
        return key_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns user_id by given session id"""
        if not session_id or not isinstance(session_id, str):
            return None
        return type(self).user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns user based on given cookie"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        User.load_from_file()
        if 'User' not in DATA:
            return None
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """delete user session"""
        session = self.session_cookie(request)
        if not session:
            return False
        user_id = self.user_id_for_session_id(session)
        if not user_id:
            return False
        del type(self).user_id_by_session_id[session]
        return True
