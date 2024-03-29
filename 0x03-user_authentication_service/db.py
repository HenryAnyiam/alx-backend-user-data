#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """queries database to find user"""
        query = self._session.query(User)
        for key, value in kwargs.items():
            column = getattr(User, key, None)
            if column:
                query = query.filter(column == value)
            else:
                raise InvalidRequestError
        result = query.all()
        if not result:
            raise NoResultFound
        return result[0]

    def update_user(self, user_id: int, **kwargs) -> None:
        """update user"""
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                if key == "id" and not isinstance(value, int):
                    raise ValueError
                elif ((key == "session_id" or key == "reset_token")
                      and not value):
                    pass
                elif key == "hashed_password":
                    if (not isinstance(value, bytes) and
                       not isinstance(value, str)):
                        raise ValueError
                elif not isinstance(value, str):
                    raise ValueError
                setattr(user, key, value)
                self._session.commit()
