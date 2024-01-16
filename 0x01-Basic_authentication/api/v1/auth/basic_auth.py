#!/usr/bin/env python3
"""Basic Authentication"""

from api.v1.auth.auth import Auth
from base64 import b64decode, binascii
from models.base import DATA
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Handle Basic Authentication
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract authorization header"""
        if (not authorization_header or
           not isinstance(authorization_header, str) or
           not (authorization_header.startswith("Basic "))):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           b64_a_header: str) -> str:
        """decode bas64 string"""
        if (not b64_a_header or
           not isinstance(b64_a_header, str)):
            return None
        try:
            return b64decode(b64_a_header.encode()).decode()
        except binascii.Error:
            return None
        except UnicodeDecodeError:
            return None

    def extract_user_credentials(self,
                                 decoded_b64_auth_header: str) -> (str, str):
        """extract user details from str"""
        if (not decoded_b64_auth_header or
           not isinstance(decoded_b64_auth_header, str) or
           (':' not in decoded_b64_auth_header)):
            return None, None
        return tuple(decoded_b64_auth_header.split(':'))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """checks for user object"""
        if not user_email or not user_pwd:
            return None
        User.load_from_file()
        if 'User' not in DATA:
            return None
        user = User.search({'email': user_email})
        if not user or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves user from a request"""
        auth = self.authorization_header(request)
        user_details = self.extract_base64_authorization_header(auth)
        decoded_details = self.decode_base64_authorization_header(user_details)
        credentials = self.extract_user_credentials(decoded_details)
        return self.user_object_from_credentials(*credentials)
