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
        return (False, "Username and password required.")
    if not re.match("^[a-z]+$", username):
        return (False, "Please use only letters a-z for username.")
    if len(username) < 2:
        return (False, "Username too short.")
    if len(password) < 6:
        return (False, "Password too short.")
    if re.match("^[a-z]+$", password):
        return (False, "Password should contain other characters than letters.")
    existing_user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    if existing_user:
        return (False, "Username already exists.")

    return (True,)


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


def get_user_id(username):
    sql_user = text("SELECT id FROM users WHERE username=:username")
    result_user = db.session.execute(sql_user, {"username": username})
    user = result_user.fetchone()

    return user.id if user else None

def check_user_exists(username):
    user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    return user