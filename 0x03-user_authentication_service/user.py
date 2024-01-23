#!/usr/bin/env python3
"""Map a class to table User"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence


Base = declarative_base()


class User(Base):
    """map class to table user"""

    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'),
                primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
