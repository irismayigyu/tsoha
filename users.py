from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import re
from sqlalchemy.sql import text
import secrets
from flask import session


def login(username, password):
    user = db.session.execute(
        text("SELECT id, username, password FROM users WHERE username = :username"), {"username": username}).fetchone()
    if not user:
        return False
    hash_value = user.password
    check_password(username, hash_value, password)

    return user


def check_password(username, hash_value, password):
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)


def logout():
    session.pop("username", None)


def validate(username, password):
    if not username or not password:
        return "error1"
    if not re.match("^[a-z]+$", username):
        return "error2"
    if len(username) < 2:
        return "error3"
    if len(password) < 6:
        return "error4"
    if re.match("^[a-z]+$", password):
        return "error5"
    existing_user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    if existing_user:
        return "error6"

    return False


def register(username, password):

    hash_value = generate_password_hash(password)

    try:
        query = text(
            "INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(
            query, {"username": username, "password": hash_value})
        db.session.commit()
    except Exception:
        return "Something went wrong"
    session["username"] = username
    return True
