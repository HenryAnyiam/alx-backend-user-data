#!/usr/bin/env python3
"""create app"""

from flask import Flask, jsonify, request, url_for
from flask import abort, make_response, redirect
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


@app.route("/sessions", methods=["POST", "DELETE"],
           strict_slashes=False)
def login():
    """login user"""
    if request.method == "DELETE":
        cookie = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(cookie)
        if not user:
            abort(403)
        else:
            AUTH.destroy_session(user.id)
            return redirect(url_for("index"))
    elif request.method == "POST":
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


@app.route("/profile", strict_slashes=False)
def profile():
    """return user profile according to session"""
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"],
           strict_slashes=False)
def get_reset_password_token():
    """get password reset token"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}",
                        "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
