from db import db
from werkzeug.security import check_password_hash, generate_password_hash
import re
from sqlalchemy.sql import text
import secrets
from flask import session
import users


def get_user_favorite_books(username):
    user_id = users.get_user_id(username)
    if not user_id:
        return []

    sql = text("SELECT b.* FROM books b "
               "JOIN favourites f ON b.id = f.book_id "
               "WHERE f.user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    fav_books = result.fetchall()

    return fav_books


def find_books():
    username = session['username']
    user_id = users.get_user_id(username)
    query_book = text(
        "SELECT * FROM books WHERE WHERE content ILIKE :query")
    result_book = db.session.execute(query_book, {"user_id": user_id})
    books = result_book.fetchall()
    return books

def query_books(name):
    query_book = text("SELECT * FROM books WHERE bookname = :name")
    result_book = db.session.execute(query_book, {"name": name})
    book = result_book.fetchone()
    return book

def add_book(user, book, name, status, grade, review, review_date):
    query = text(
    "INSERT INTO reviews (user_id, book_id, name, status, grade, review, review_date)"
    " VALUES (:user_id, :book_id, :name, :status, :grade, :review, :review_date)"
    " ON CONFLICT (user_id, book_id) DO UPDATE"
    " SET name = :name, status = :status, grade = :grade, review = :review, review_date = :review_date")
    db.session.execute(query, {"user_id": user.id, "book_id": book.id, "name": name,
                            "status": status, "grade": grade, "review": review, "review_date": review_date})
    db.session.commit()

def check_existing_favourite(user_id, book_id):
    sql = text(
        "SELECT id FROM favourites WHERE user_id=:user_id AND book_id=:book_id")
    existing_favourite = db.session.execute(
        sql, {"user_id": user_id, "book_id": book_id}).scalar()

    return existing_favourite is not None


def add_book_to_favourites(user_id, book_id):
    query = text(
        "INSERT INTO favourites (user_id, book_id) VALUES (:user_id, :book_id)")
    db.session.execute(query, {"user_id": user_id, "book_id": book_id})
    db.session.commit()

def delete_book_from_favourites(user_id, book_id):
    query = text(
        "DELETE from favourites WHERE user_id=:user_id AND book_id=:book_id")
    db.session.execute(query, {"user_id": user_id, "book_id": book_id})
    db.session.commit()


def search_books(query):
    sql = text(
        "SELECT * FROM books WHERE bookname LIKE :query OR author LIKE :query")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    found_books = result.fetchall()
    return found_books