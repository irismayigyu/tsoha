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
    if not re.match("^[A-Za-z]+$", username):
        return (False, "Please use only letters A-z for username.")
    if len(username) < 3:
        return (False, "Username too short.")
    if len(password) < 5:
        return (False, "Password too short.")
    if re.match("^[A-Za-z]+$", password):
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


def select_user(username):
    user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    return user


def showusers(query):
    sql = text("SELECT username FROM users WHERE username LIKE :query")
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    found_users = result.fetchall()
    return found_users


def foundfriends(user):
    sql_friends = text("""SELECT DISTINCT f1.user2
                   FROM friends f1, friends f2
                   WHERE f1.user1 = :user AND
                         f1.user1 = f2.user2 AND
                         f1.user2 = f2.user1;""")

    result_friends = db.session.execute(sql_friends, {"user": user})
    found_friends = result_friends.fetchall()
    return found_friends


def foundreviews(friend_id):
    sql_reviews = text("""SELECT r.id, r.name, r.status, r.grade, r.review, r.review_date
                        FROM reviews r
                        WHERE r.user_id = :friend_id""")
    result_reviews = db.session.execute(sql_reviews, {"friend_id": friend_id})
    reviews = result_reviews.fetchall()
    return reviews


def check_friends(current_user, viewed_user):
    sql = text(
        "SELECT * FROM friends WHERE user1=:current_user AND user2=:viewed_user")
    result = db.session.execute(
        sql, {"current_user": current_user, "viewed_user": viewed_user})
    results = len(result.fetchall())
    return results


def add_connection(current_user, viewed_user):
    query = text(
        "INSERT INTO friends (user1, user2) VALUES (:current_user, :viewed_user)")
    db.session.execute(
        query, {"current_user": current_user, "viewed_user": viewed_user})
    db.session.commit()


def delete_connection(current_user, viewed_user):
    query = text(
        "DELETE FROM friends WHERE user1=:current_user AND user2=:viewed_user")
    db.session.execute(
        query, {"current_user": current_user, "viewed_user": viewed_user})
    db.session.commit()


def select_user_reviews(user):
    query_reviews = text("SELECT * FROM reviews WHERE user_id = :user_id")
    result_reviews = db.session.execute(query_reviews, {"user_id": user.id})
    user_reviews = result_reviews.fetchall()
    return user_reviews
