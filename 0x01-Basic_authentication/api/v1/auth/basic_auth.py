#!/usr/bin/env python3
"""Basic Authentication"""

from api.v1.auth.auth import Auth


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
