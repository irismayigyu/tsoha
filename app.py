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

        if not username or not password:
            return "Please enter a valid username or password <a href='/register'>Try again</a>"

        existing_user = db.session.execute(
            text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
        if existing_user:
            return "Username already exists."
        hash_value = generate_password_hash(password)
        try:
            query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(query, {"username": username, "password": hash_value})
            db.session.commit()
        except Exception as e:
            print(e)
            return "Registration failed"
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
    status = request.form["status"]
    grade = request.form["grade"]
    review = request.form["review"]
    print("print")
    return render_template("result.html", status=status,
                                        grade=grade,
                                        review=review)

@app.route("/search")
def search():
    return render_template("search.html")



