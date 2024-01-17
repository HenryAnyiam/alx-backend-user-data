#!/usr/bin/env python3
"""Module to handle Session Based Authentication"""

from uuid import uuid4
from api.v1.auth.auth import Auth


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
