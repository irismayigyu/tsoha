
from db import db
from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from sqlalchemy.sql import text
from app import app
import re


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
        return "Username not found. <a href='/'>Try again</a>"

    hash_value = user.password
    if check_password_hash(hash_value, password):
        session["username"] = username
        return redirect("/startpage")

    else:
        return "Incorrect password. <a href='/'>Try again</a>"


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


def validate(username, password): 
    if not username or not password:
        return "Username and password are required"
    if not re.match("^[a-z]+$", username):
        return "Please use only letters a-z for username. <a href='/register'>Try again</a>"
    if len(username) < 2:
        return "Username too short. <a href='/register'>Try again</a>"
    if len(password) < 6:
        return "Password too short. <a href='/register'>Try again</a>"
    if re.match("^[a-z]+$", password):
        return "Password should contain other characters than letters. <a href='/register'>Try again</a>"


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
            return "Username already exists. <a href='/register'>Try again</a>"
        hash_value = generate_password_hash(password)

        try:
            query = text(
                "INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(
                query, {"username": username, "password": hash_value})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Registration failed. <a href='/register'>Try again</a>"
        session["username"] = username
        return redirect("/")
def get_user_favorite_books(username):
    user_id = get_user_id(username)

    if not user_id:
        return []

    # Fetch favorite books for the user
    sql = text("SELECT b.* FROM books b "
               "JOIN favourites f ON b.id = f.book_id "
               "WHERE f.user_id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id})
    fav_books = result.fetchall()

    return fav_books

@app.route("/startpage")
def startpage():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"

    username = session["username"]
    user_id = get_user_id(username)
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
        return "User not logged in. <a href='/'>Login</a>"
    return render_template("addreview.html", name=bookname)


@app.route("/savedreview", methods=["POST"])
def savedreview():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    name = request.form["name"]
    status = request.form["status"]
    grade = request.form["grade"]
    review = request.form["review"]

    username = session['username']
    query_user = text("SELECT * FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    if not user:
        return "User not found. <a href='/addreview'>Try again</a>"

    query_book = text("SELECT * FROM books WHERE bookname = :name")
    result_book = db.session.execute(query_book, {"name": name})
    book = result_book.fetchone()

    if not book:
        return "Book not found. Please add it to the database: <a href='/addbook'>Add book</a> or try again: <a href='/addreview'>Make review</a>"

    try:
        query = text(
            "INSERT INTO reviews (user_id, book_id, name, status, grade, review) VALUES (:user_id, :book_id, :name, :status, :grade, :review)")
        db.session.execute(query, {"user_id": user.id, "book_id": book.id, "name": name,
                           "status": status, "grade": grade, "review": review})
        db.session.commit()

        return render_template("savedreview.html", name=name, status=status, grade=grade, review=review)

    except Exception as e:
        print(e)
        return "Something went wrong. <a href='/addreview'>Try again</a>"


@app.route("/search")
def search():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    return render_template("search.html")


@app.route("/myreviews")
def myreviews():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    user_reviews = get_user_reviews()

    if isinstance(user_reviews, str):
        return render_template("myreviews.html", error_message=user_reviews)

    return render_template("myreviews.html", user_reviews=user_reviews)


def get_user_reviews():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"

    username = session['username']

    query_user = text("SELECT * FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

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
        return "User not logged in. <a href='/'>Login</a>"

    username = session['username']

    query_user = text("SELECT id, username, password FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    if not user:
        return "User not found. <a href='/register'>Register</a>"
    query = request.args["query"]
    query_book = text("SELECT * FROM books WHERE WHERE content LIKE :query")
    result_book = db.session.execute(query_book, {"user_id": user.id})
    books = result_book.fetchall()

    if not books:
        return "No reviews found. <a href='/startpage'>Back to main page</a>"

    return books



@app.route("/showbooks", methods=['GET', 'POST'])
def showbooks():
    username = session.get('username')
    if not username:
        return "User not logged in. <a href='/'>Login</a>"
    if request.method == 'POST':
        user_id = get_user_id(username)
        if not user_id:
            return "User not found. <a href='/'>Login</a>"
        book_id = request.form.get('book_id')
        existing_favourite = check_existing_favourite(user_id, book_id)
        if existing_favourite:
            return "Book already in favourite <a href='/startpage'>Back to main page</a"
        try:
            add_book_to_favourites(user_id, book_id)
            return "Book added to favourites successfully <a href='/startpage'>Back to main page</a"
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        query = request.args.get("query", "")
        found_books = search_books(query)

        if not found_books:
            return "Book not found. Please add it to the database: <a href='/addbook'>Add book</a> or try search again: <a href='/search'>Search</a>"

        return render_template("showbooks.html", found_books=found_books)




def check_existing_favourite(user_id, book_id):
    sql = text("SELECT id FROM favourites WHERE user_id=:user_id AND book_id=:book_id")
    existing_favourite = db.session.execute(sql, {"user_id": user_id, "book_id": book_id}).scalar()

    return existing_favourite is not None


def add_book_to_favourites(user_id, book_id):
    query = text("INSERT INTO favourites (user_id, book_id) VALUES (:user_id, :book_id)")
    db.session.execute(query, {"user_id": user_id, "book_id": book_id})
    db.session.commit()


def search_books(query):
    sql = text("SELECT * FROM books WHERE bookname LIKE :query OR author LIKE :query")
    result = db.session.execute(sql, {"query": "%" + query + "%"})
    found_books = result.fetchall()
    return found_books


@app.route("/showusers")
def showusers():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    query = request.args["query"]
    sql = text("SELECT username FROM users WHERE username LIKE :query")
    result = db.session.execute(sql, {"query": "%"+query+"%"})
    found_users = result.fetchall()
    if not found_users:
        return "No users found. Try again: <a href='/search'>Search</a>"

    return render_template("showusers.html", found_users=found_users)

@app.route("/showfriends")
def showfriends():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    user = session["username"] #ei toimi
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
        return "No friends yet."
    return render_template("showfriends.html", found_friends=found_friends, session_user=user)

@app.route("/userprofile/<username>", methods=['GET', 'POST'])
def userprofile(username):
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
    query_user = text("SELECT * FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    current_user = session["username"]
    if not user:
        return "User not found. <a href='/startpage'>Back to main page</a>"
    if request.method == 'POST':
        connect = request.form.get('connect')
        viewed_user = request.form.get('viewed_user')

        sql = text(
            "SELECT user1, user2 FROM friends WHERE user1=:current_user AND user2=:viewed_user") #tarkista löytyykö jo tietokannasta
        result = db.session.execute(
            sql, {"current_user": current_user, "viewed_user": viewed_user})
        any = len(result.fetchall())
        if any == 0 and connect == "yes":
            query = text(
                "INSERT INTO friends (user1, user2) VALUES (:current_user, :viewed_user)")
            db.session.execute(
                query, {"current_user": current_user, "viewed_user": viewed_user})
            db.session.commit()

        sql = text(
            "SELECT * FROM friends WHERE user1=:current_user AND user2=:viewed_user")
        result = db.session.execute(
            sql, {"current_user": current_user, "viewed_user": viewed_user})
        any = len(result.fetchall())
        if any > 0 and connect == "no":
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
        return "User not logged in. <a href='/'>Login</a>"
    return render_template("addbook.html")


@app.route("/savedbook", methods=["POST"])
def savedbook():
    if "username" not in session:
        return "User not logged in. <a href='/'>Login</a>"
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
    any = len(result.fetchall())
    if any > 0:
        return "Book already in database. <a href='/startpage'>Back to main page</a>"
    else:
        try:
            query = text(
                "INSERT INTO books (bookname, author, year) VALUES (:bookname, :author, :year)")
            db.session.execute(query, {"bookname": bookname,
                                       "author": author, "year": year})
            db.session.commit()

            return render_template("savedbook.html", bookname=bookname, author=author, year=year)

        except Exception as e:
            print(e)
            return "Something went wrong. <a href='/addbook'>Try again</a>"

