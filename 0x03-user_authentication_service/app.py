#!/usr/bin/env python3
"""create app"""

from flask import Flask, jsonify, request
from flask import abort, make_response
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index() -> str:
    """index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """add users"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        res = jsonify({"message": "email already registered"})
        return res, 400
    else:
        res = jsonify({"email": f"{email}",
                       "message": "user created"})
        return res, 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """login user"""
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if user:
        session_id = AUTH.create_session(email)
        res = make_response({"email": f"{email}",
                             "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
