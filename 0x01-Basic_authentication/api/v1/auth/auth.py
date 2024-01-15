#!/usr/bin/env python3
"""Manage API Authentication
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """reuire authentication"""
        if not path or not excluded_paths:
            return True
        if ((path in excluded_paths) or
           ((path + '/') in excluded_paths)):
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None