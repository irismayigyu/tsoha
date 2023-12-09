
from db import db
from flask import redirect, render_template, request, session, Flask, flash
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from app import app
import re
import secrets


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.session.execute(
        text("SELECT id, username, password FROM users WHERE username = :username"), {"username": username}).fetchone()
    if not user:
        return render_template("error.html", username=username, hint="Username not found.")

    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/startpage")

    return render_template("error.html", username=username, hint="Incorrect password.")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")


def validate(username, password):
    if not username or not password:
        return render_template("error.html", username=username, hint="Username and password required.")
    if not re.match("^[a-z]+$", username):
        return render_template("error.html", hint="Please use only letters a-z for username.")
    if len(username) < 2:
        return render_template("error.html", hint="Username too short.")
    if len(password) < 6:
        return render_template("error.html", hint="Password too short.")
    if re.match("^[a-z]+$", password):
        return render_template("error.html", hint="Password should contain other characters than letters.")
    return True


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validation = validate(username, password)
        if validation:
            return validation

        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
        if existing_user:
            return render_template("error.html", username="username", hint="Username already exists.")
        hash_value = generate_password_hash(password)

        try:
            query = text(
                "INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(
                query, {"username": username, "password": hash_value})
            db.session.commit()
        except Exception:
            return render_template("error.html", username="username", hint="Something went wrong.")
        session["username"] = username
        return redirect("/")
    return False


def get_user_favorite_books(username):
    user_id = get_user_id(username)

    if not user_id:
        return []

    sql = text("SELECT b.* FROM books b "
               "JOIN favourites f ON b.id = f.book_id "
               "WHERE f.user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    fav_books = result.fetchall()

    return fav_books


@app.route("/startpage")
def startpage():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    username = session["username"]
    #user_id = get_user_id(username)
    fav_books = get_user_favorite_books(username)
    return render_template("startpage.html", fav_books=fav_books)


def get_user_id(username):
    sql_user = text("SELECT id FROM users WHERE username=:username")
    result_user = db.session.execute(sql_user, {"username": username})
    user = result_user.fetchone()

    return user.id if user else None


@app.route("/addreview/<bookname>")
def addreview(bookname):
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    return render_template("addreview.html", name=bookname)


def check_user_exists(username):
    user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
    # query_user = text("SELECT * FROM users WHERE username = :username")
    # result_user = db.session.execute(query_user, {"username": username})
    # user = result_user.fetchone()
    if not user:
        return render_template("error.html", username="username", hint="User not found.")
    return user


@app.route("/savedreview", methods=["POST"])
def savedreview():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html")
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    name = request.form["name"]
    status = request.form["status"]
    grade = request.form["grade"]
    review = request.form["review"]

    username = session['username']
    user = check_user_exists(username)
    query_book = text("SELECT * FROM books WHERE bookname = :name")
    result_book = db.session.execute(query_book, {"name": name})
    book = result_book.fetchone()

    if not book:
        return render_template("error.html", hint="Book not found. Please add it to the database or try again.")

    try:
        query = text(
            "INSERT INTO reviews (user_id, book_id, name, status, grade, review)"
            " VALUES (:user_id, :book_id, :name, :status, :grade, :review)")
        db.session.execute(query, {"user_id": user.id, "book_id": book.id, "name": name,
                                   "status": status, "grade": grade, "review": review})
        db.session.commit()

        return render_template("savedreview.html", name=name, status=status, grade=grade, review=review)

    except Exception:
        return "Something went wrong. <a href='/addreview'>Try again</a>"


@app.route("/search")
def search():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    return render_template("search.html")


@app.route("/myreviews")
def myreviews():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    user_reviews = get_user_reviews()

    if isinstance(user_reviews, str):
        return render_template("myreviews.html", error_message=user_reviews)

    return render_template("myreviews.html", user_reviews=user_reviews)


def get_user_reviews():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    username = session['username']
    user = check_user_exists(username)

    if not user:
        return redirect("/")

    query_reviews = text("SELECT * FROM reviews WHERE user_id = :user_id")
    result_reviews = db.session.execute(query_reviews, {"user_id": user.id})
    user_reviews = result_reviews.fetchall()

    if not user_reviews:
        return "No reviews found."

    return user_reviews


def find_books():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    username = session['username']

    # query_user = text(
    #     "SELECT id, username, password FROM users WHERE username = :username")
    # result_user = db.session.execute(query_user, {"username": username})
    # user = result_user.fetchone()

    # if not user:
    #     return "User not found. <a href='/register'>Register</a>"

    user = check_user_exists(username)
    if user:
        #query = request.args["query"]
        query_book = text(
            "SELECT * FROM books WHERE WHERE content LIKE :query")
        result_book = db.session.execute(query_book, {"user_id": user.id})
        books = result_book.fetchall()

        if not books:
            return render_template("error.html", username="username", hint="No books found.")

        return books
    return False


@app.route("/showbooks", methods=['GET', 'POST'])
def showbooks():
    username = session.get('username')
    if not username:
        return render_template("error.html", username="username", hint="User not logged in.")
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return "Something went wrong. <a href='/'>Try again</a>"
        user_id = get_user_id(username)
        if not user_id:
            return "User not found. <a href='/'>Login</a>"
        book_id = request.form.get('book_id')
        existing_favourite = check_existing_favourite(user_id, book_id)
        if existing_favourite:
            return render_template("error.html", username="username", hint="Book already in favourites")

        try:
            add_book_to_favourites(user_id, book_id)
            return render_template("error.html", username="username", hint="Book added to favourites successfully")
        except Exception:
            return False

    query = request.args.get("query", "")
    found_books = search_books(query)

    if not found_books:
        return render_template("error.html", username="username", hint="Book not found. Add it or search again.")

    return render_template("showbooks.html", found_books=found_books)


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


def search_books(query):
    sql = text(
        "SELECT * FROM books WHERE bookname LIKE :query OR author LIKE :query")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    found_books = result.fetchall()
    return found_books


@app.route("/showusers")
def showusers():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    query = request.args["query"]
    sql = text("SELECT username FROM users WHERE username LIKE :query")
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    found_users = result.fetchall()
    if not found_users:
        return render_template("error.html", username="username", hint="No users found")

    return render_template("showusers.html", found_users=found_users)


@app.route("/showfriends")
def showfriends():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    user = session["username"]  # ei toimi
    sql = text("SELECT DISTINCT user1 AS friend1, user2 AS friend2 "
               "FROM friends f1 WHERE (:user IN (f1.user1, f1.user2)) "
               "AND EXISTS (SELECT 1 FROM friends f2 WHERE "
               "(:user IN (f2.user1, f2.user2) AND "
               "((f1.user1=f2.user1 AND f1.user2=f2.user2) OR "
               "(f1.user1=f2.user2 AND f1.user2=f2.user1))))")

    result = db.session.execute(sql, {"user": user})

    found_friends = result.fetchall()
    print(found_friends)
    if not found_friends:
        return render_template("error.html", hint="No friends yet.")
    return render_template("showfriends.html", found_friends=found_friends, session_user=user)


@app.route("/userprofile/<username>", methods=['GET', 'POST'])
def userprofile(username):
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    username = session['username']
    user = check_user_exists(username)

    current_user = session["username"]
    if not user:
        return "User not found. <a href='/startpage'>Back to main page</a>"
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", username="username", hint="Invalid CSRF token.")
        connect = request.form.get('connect')
        viewed_user = request.form.get('viewed_user')

        sql = text(
            "SELECT user1, user2 FROM friends WHERE user1=:current_user AND user2=:viewed_user")
        result = db.session.execute(
            sql, {"current_user": current_user, "viewed_user": viewed_user})
        found = len(result.fetchall())
        if found == 0 and connect == "yes":
            query = text(
                "INSERT INTO friends (user1, user2) VALUES (:current_user, :viewed_user)")
            db.session.execute(
                query, {"current_user": current_user, "viewed_user": viewed_user})
            db.session.commit()

        sql = text(
            "SELECT * FROM friends WHERE user1=:current_user AND user2=:viewed_user")
        result = db.session.execute(
            sql, {"current_user": current_user, "viewed_user": viewed_user})
        found = len(result.fetchall())
        if found > 0 and connect == "no":
            query = text(
                "DELETE FROM friends WHERE user1=:current_user AND user2=:viewed_user")
            db.session.execute(
                query, {"current_user": current_user, "viewed_user": viewed_user})
            db.session.commit()
# tee nii et ei voi olla ittensä frendi.
    return render_template("userprofile.html", user=user)


@app.route("/addbook")
def addbook():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    return render_template("addbook.html")


@app.route("/savedbook", methods=["POST"])
def savedbook():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", username="username", hint="Invalid CSRF token.")
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    bookname = request.form["bookname"]
    author = request.form["author"]
    year = request.form["year"]

    username = session['username']
    query_user = text("SELECT username FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    if not user:
        return "User not found."
    sql = text("SELECT * FROM books WHERE bookname=:bookname")
    result = db.session.execute(sql, {"bookname": bookname})
    found = len(result.fetchall())
    if found > 0:
        return render_template("error.html", hint="Book already in database.")
    try:
        query = text(
            "INSERT INTO books (bookname, author, year) VALUES (:bookname, :author, :year)")
        db.session.execute(query, {"bookname": bookname,
                                   "author": author, "year": year})
        db.session.commit()

        return render_template("savedbook.html", bookname=bookname, author=author, year=year)

    except Exception:
        return "Something went wrong. <a href='/addbook'>Try again</a>"
