#!/usr/bin/env python3
"""Manage API Authentication
"""

from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reuire authentication"""
        if not path or not excluded_paths:
            return True
        if ((path in excluded_paths) or
           ((path + '/') in excluded_paths)):
            return False
        for i in excluded_paths:
            if i[:-1] in path and i[-1] == '*':
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if not request or not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None

    def session_cookie(self, request=None):
        """return session cookie"""
        cookie_name = getenv("SESSION_NAME")
        if not request or not cookie_name:
            return None
        return request.cookies.get(cookie_name)
