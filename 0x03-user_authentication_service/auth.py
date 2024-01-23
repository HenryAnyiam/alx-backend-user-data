#!/usr/bin/env python3
"""User authentication"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password using bcrypt"""
    encoded = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(encoded, salt)
    return hashed
