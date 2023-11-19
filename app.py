from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from sqlalchemy.sql import text


app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
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

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
        if existing_user:
            return "Username already exists. <a href='/register'>Try again</a>"
        hash_value = generate_password_hash(password)
        try:
            query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(query, {"username": username, "password": hash_value})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Registration failed. <a href='/register'>Try again</a>"
        session["username"] = username
        return redirect("/")


@app.route("/startpage")
def startpage():
    return render_template("startpage.html")

@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/result", methods=["POST"])
def result():

    name = request.form["name"]
    status = request.form["status"]
    grade = request.form["grade"]
    review = request.form["review"]

    username = session['username']
    query_user = text("SELECT * FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    if not user:
        return "User not found."

    try:
        query = text("INSERT INTO books (user_id, name, status, grade, review) VALUES (:user_id, :name, :status, :grade, :review)")
        db.session.execute(query, {"user_id": user.id, "name": name, "status": status, "grade": grade, "review": review})
        db.session.commit()

        return render_template("result.html", name=name, status=status, grade=grade, review=review)

    except Exception as e:
        print(e)
        return "Insertion failed. <a href='/form'>Try again</a>"

@app.route("/search")
def search():
    query = request.args["query"]
    sql = "SELECT * FROM books WHERE name LIKE :query OR status LIKE :query OR grade LIKE :query OR review LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    books = result.fetchall()
    return render_template("search.html", books=books)


@app.route("/mybooks")
def mybooks():
    user_books = get_user_books()

    if isinstance(user_books, str):
        return render_template("mybooks.html", error_message=user_books)

    return render_template("mybooks.html", user_books=user_books)

def get_user_books():
    if 'username' not in session:
        return "User not logged in."

    username = session['username']

    query_user = text("SELECT * FROM users WHERE username = :username")
    result_user = db.session.execute(query_user, {"username": username})
    user = result_user.fetchone()

    if not user:
        return "User not found."

    query_books = text("SELECT * FROM books WHERE user_id = :user_id")
    result_books = db.session.execute(query_books, {"user_id": user.id})
    user_books = result_books.fetchall()

    if not user_books:
        return "No books found."

    return user_books



