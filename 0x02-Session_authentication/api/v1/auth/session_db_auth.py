#!/usr/bin/env python3
"""Modue to handle Session DB auth
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Session database Authentication
    """

    def create_session(self, user_id=None):
        """create user session"""
        key_id = super().create_session(user_id)
        if user_id and key_id:
            kwargs = {"user_id": user_id,
                      "session_id": key_id}
            user_session = UserSession(**kwargs)
            user_session.save()
        return key_id

    def user_id_for_session_id(self, session_id=None):
        """overload parent method"""
        if session_id:
            session_dict = type(self).user_id_by_session_id[session_id]
            exp = session_dict["created_at"]
            exp += timedelta(seconds=self.session_duration)
            if exp < datetime.now():
                self.destroy_session()
                return None
            user = UserSession.search({"session_id": session_id})
            if user:
                return user[0].user_id
        return None

    def destroy_session(self, request=None):
        """destroy saved session"""
        session = self.session_cookie(request)
        if not session:
            return False
        user_id = self.user_id_for_session_id(session)
        if not user_id:
            return False
        user = UserSession.get(user_id)
        if user:
            user.remove()
        del type(self).user_id_by_session_id[session]
        return True
