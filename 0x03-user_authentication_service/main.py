#!/usr/bin/env python3
"""assert tests for web server"""

import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """register user"""
    body = {
            "email": email,
            "password": password
            }
    res = requests.post(url="http://localhost:5000/users",
                        data=body)
    result = {"email": f"{email}",
              "message": "user created"}
    assert res.status_code == 200
    assert res.json() == result


def log_in_wrong_password(email: str, password: str) -> None:
    """test login with the wrong password"""
    body = {
            "email": email,
            "password": password
            }
    res = requests.post(url="http://localhost:5000/sessions",
                        data=body)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """log in user"""
    body = {
            "email": email,
            "password": password
            }
    res = requests.post(url="http://localhost:5000/sessions",
                        data=body)
    result = {"email": f"{email}",
              "message": "logged in"}
    assert res.status_code == 200
    assert res.json() == result
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """test for unlogged profile"""
    cookie = {"session_id": None}
    res = requests.get(url="http://localhost:5000/profile",
                       cookies=cookie)
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """test for logged profile"""
    cookie = {"session_id": session_id}
    res = requests.get(url="http://localhost:5000/profile",
                       cookies=cookie)
    email = res.json().get("email")
    assert res.status_code == 200
    assert res.json() == {"email": f"{email}"}


def log_out(session_id: str) -> None:
    """test user log out functionality"""
    cookie = {"session_id": session_id}
    res = requests.delete(url="http://localhost:5000/sessions",
                          cookies=cookie, allow_redirects=True)
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """test for reset password functionality"""
    body = {"email": email}
    res = requests.post(url="http://localhost:5000/reset_password",
                        data=body)
    token = res.json().get("reset_token")
    result = {"email": f"{email}",
              "reset_token": f"{token}"}
    assert res.status_code == 200
    assert res.json() == result
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password functionality"""
    body = {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    res = requests.put(url="http://localhost:5000/reset_password",
                       data=body)
    result = {"email": f"{email}",
              "message": "Password updated"}
    assert res.status_code == 200
    assert res.json() == result


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
