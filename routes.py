
from db import db
from flask import redirect, render_template, request, session, Flask, flash
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import app
import secrets
import users
import books
from datetime import datetime
from users import select_user as users_select_user


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.login(username, password)
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
    users.logout()
    return redirect("/")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        validation = users.validate(username, password)
        if validation[0] is False:
            return render_template("error.html", username=username, hint=validation[1])
        users.register(username, password)
        return redirect("/")
    return False


def get_user_favorite_books(username):
    user_id = users.get_user_id(username)
    if not user_id:
        return []
    fav_books = books.get_user_favorite_books(username)
    return fav_books


@app.route("/startpage", methods=["POST", "GET"])
def startpage():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    username = session["username"]

    user_id = users.get_user_id(username)
    if not user_id:
        return render_template("error.html", username="username", hint="User not found.")
    fav_books = get_user_favorite_books(username)
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", username="username", hint="Something went wrong..")
        user_id = users.get_user_id(username)
        if not user_id:
            return render_template("error.html", username="username", hint="User not found.")
        book_id = request.form.get('book_id')
        existing_favourite = books.check_existing_favourite(user_id, book_id)
        if existing_favourite:
            books.delete_book_from_favourites(user_id, book_id)
            return render_template("error.html", username="username", hint="Book removed from favourites")
        if not existing_favourite:
            return render_template("error.html", username="username", hint="Book is not in favourites")
    return render_template("startpage.html", fav_books=fav_books)


@app.route("/addreview/<bookname>")
def addreview(bookname):
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    review_date = datetime.now().strftime("%Y-%m-%d")
    return render_template("addreview.html", name=bookname, review_date=review_date)


def check_user_exists(username):
    user = users_select_user(username)
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
    review_date = request.form["review_date"]

    username = session['username']
    user = check_user_exists(username)

    book = books.query_books(name)

    if not book:
        return render_template("error.html", hint="Book not found. Please add it to the database or try again.")

    try:
        books.add_book(user, book, name, status, grade, review, review_date)
        return render_template("savedreview.html", name=name, status=status, grade=grade, review=review, review_date=review_date)

    except Exception:
        return render_template("error.html", username="username", hint="Something went wrong..")


@app.route("/search")
def search():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    username = session['username']
    user_id = users.get_user_id(username)
    if not user_id:
        return render_template("error.html", username="username", hint="User not found.")
    return render_template("search.html")


@app.route("/myreviews", methods=["GET", "POST"])
def myreviews():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    username = session['username']
    user_id = users.get_user_id(username)
    if not user_id:
        return render_template("error.html", username="username", hint="User not found.")
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", username="username", hint="Something went wrong..")
        review_id = request.form.get('review_id')
        books.delete_review(user_id, review_id)
        return render_template("error.html", username="username", hint="Review has been deleted")

    user_reviews = get_user_reviews()
    review_average = books.get_rev_avg(user_id)
    count = books.get_rev_count(user_id)
    if isinstance(user_reviews, str):
        return render_template("myreviews.html", error_message=user_reviews)

    return render_template("myreviews.html", user_reviews=user_reviews, review_average=review_average, count=count)


def get_user_reviews():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    username = session['username']
    user = check_user_exists(username)

    if not user:
        return redirect("/")
    user_reviews = users.select_user_reviews(user)

    if not user_reviews:
        return "No reviews found."

    return user_reviews


def find_books():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    username = session['username']
    user = check_user_exists(username)
    if user:
        found = books.find_books()
        if not found:
            return render_template("error.html", username="username", hint="No books found.")
        return found
    return False


@app.route("/showbooks", methods=['GET', 'POST'])
def showbooks():
    username = session.get('username')
    if not username:
        return render_template("error.html", username="username", hint="User not logged in.")
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", username="username", hint="Something went wrong..")
        user_id = users.get_user_id(username)
        if not user_id:
            return render_template("error.html", username="username", hint="User not found.")
        book_id = request.form.get('book_id')
        existing_favourite = books.check_existing_favourite(user_id, book_id)
        if not existing_favourite:
            books.add_book_to_favourites(user_id, book_id)
            return render_template("error.html", username="username", hint="Book added to favourites")
        if existing_favourite:
            return render_template("error.html", username="username", hint="Book already in favourites")

    query = request.args.get("query", "")
    found_books = books.search_books(query)

    if not found_books:
        return render_template("error.html", username="username", hint="Book not found. Add it or search again.")

    return render_template("showbooks.html", found_books=found_books)


@app.route("/showusers")
def showusers():
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    query = request.args["query"]
    found_users = users.showusers(query)
    if not found_users:
        return render_template("error.html", username="username", hint="No users found")

    return render_template("showusers.html", found_users=found_users)


@app.route("/showfriends", methods=['GET', 'POST'])
def showfriends():

    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")

    user = session["username"]
    username = session['username']
    user_id = users.get_user_id(username)
    if not user_id:
        return render_template("error.html", username="username", hint="User not found.")
    found_friends = users.foundfriends(user)

    friend_reviews = []

    for friend in found_friends:
        friend_id = users.get_user_id(friend[0])
        if friend_id:
            reviews = users.foundreviews(friend_id)
            friend_reviews.append(
                {"friend_username": friend[0], "reviews": reviews})
    if request.method == 'POST':
        # if session["csrf_token"] != request.form["csrf_token"]:
        #     return render_template("error.html", username="username", hint="Invalid CSRF token.")
        viewed_user = request.form.get('viewed_user')
        found = users.check_friends(username, viewed_user)
        if found > 0:
            users.delete_connection(username, viewed_user)
            return render_template("error.html", username="username", hint="You have removed connection")

    if not found_friends:
        return render_template("error.html", hint="No friends yet.")
    return render_template("showfriends.html", found_friends=friend_reviews, session_user=user)


@app.route("/userprofile/<username>", methods=['GET', 'POST'])
def userprofile(username):
    if "username" not in session:
        return render_template("error.html", username="username", hint="User not logged in.")
    user = users_select_user(username)

    current_user = session["username"]
    if not user:
        return render_template("error.html", username="username", hint="User not found.")
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            return render_template("error.html", username="username", hint="Invalid CSRF token.")
        viewed_user = request.form.get('viewed_user')
        found = users.check_friends(current_user, viewed_user)
        if not found:
            users.add_connection(current_user, viewed_user)
            return render_template("error.html", username="username", hint="You have connected")
        if found:
            return render_template("error.html", username="username", hint="You have already connected")
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
    user = users_select_user(username)
    if not user:
        return render_template("error.html", username="username", hint="User not found.")
    found = books.found_books(bookname)
    if found > 0:
        return render_template("error.html", hint="Book already in database.")
    try:
        books.insert_book(bookname, author, year)
        return render_template("savedbook.html", bookname=bookname, author=author, year=year)

    except Exception:
        return render_template("error.html", username="username", hint="Something went wrong..")
