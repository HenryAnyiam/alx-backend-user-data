#!/usr/bin/env python3
"""New authentication system"""

from models.base import Base


class UserSession(Base):
    """user session"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize User Session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
