#!/usr/bin/env python3
"""Module app"""
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=['GET'], strict_slashes=False)
def status() -> str:
    """Basic flask app"""
    return jsonify({"Status": "OK"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    end-point to register a user
    Test on terminal:
        curl -XPOST localhost:5000/users -d
        'email=bob@me.com' -d 'password=mySuperPwd' -v
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email, password)
        # used AUTH. DB is a lower abstraction that is proxied by Auth
        if new_user is not None:
            return jsonify({
                "email": new_user.email,
                "message": "user created"
                })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login Route
    create a new session for the user, store it the session ID as a cookie
    with key "session_id" on the response and
    return a JSON payload of the form
    """
    email = request.form.get("email")
    password = request.form.get("password")
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    The request is expected to contain the session ID as a cookie
    with key "session_id".
    Find the user with the requested session ID.
    If the user exists destroy the session and redirect the user to GET /.
    If the user does not exist, respond with a 403 HTTP status.
    """
    s_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(s_cookie)
    if s_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist, respond with a
    200 HTTP status
    """
    s_cookie = request.cookies.get("session_id", None)
    if s_cookie is None:
        abort(403)
    user = AUTH.get_user_from_session_id(s_cookie)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    If the email is not registered, it responds with a 403 status code.
    Otherwise, it generate a token and responds with a 200 HTTP status
    """
    u_email = request.form.get("email")
    is_registered = AUTH.create_session(u_email)
    if not is_registered:
        abort(403)

    reset_pswd = AUTH.get_reset_password_token(u_email)
    return jsonify({"email": u_email, "reset_token": reset_pswd})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Updates the password.
    If the token is invalid, catch the exception and respond with a
    403 HTTP code.If the token is valid, respond with a 200 HTTP code
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")