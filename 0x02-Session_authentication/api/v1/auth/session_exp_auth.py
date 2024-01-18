#!/usr/bin/env python3
"""Module to handle
Seesion ID expiration"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Handle session expiration"""

    def __init__(self):
        self.session_duration = getenv("SESSION_DURATION", 0)
        if self.session_duration:
            try:
                self.session_duration = int(self.session_duration)
            except ValueError:
                self.session_duration = 0

    def create_session(self, user_id=None):
        """create user session"""
        key_id = super().create_session(user_id)
        if not key_id:
            return None
        session_dict = {"user_id": user_id,
                        "created_at": datetime.now()}
        type(self).user_id_by_session_id[key_id] = session_dict
        return key_id

    def user_id_for_session_id(self, session_id=None):
        """overload parent method"""
        if ((not session_id) or
           (session_id not in type(self).user_id_by_session_id)):
            return None
        session_dict = type(self).user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if "created_at" not in session_dict:
            return None
        exp = session_dict["created_at"]
        exp += timedelta(seconds=self.session_duration)
        print(exp, datetime.now())
        if exp < datetime.now():
            return None
        return session_dict["user_id"]
