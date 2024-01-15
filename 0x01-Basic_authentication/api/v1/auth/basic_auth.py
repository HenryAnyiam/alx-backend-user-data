#!/usr/bin/env python3
"""Basic Authentication"""

from api.v1.auth.auth import Auth
from base64 import b64decode, binascii


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
