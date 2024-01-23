#!/usr/bin/env python3
"""create app"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
