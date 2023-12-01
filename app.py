
# from flask import redirect, render_template, request, session
from os import getenv
# from werkzeug.security import check_password_hash, generate_password_hash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import text
from flask import Flask
from flask import flash



app = Flask(__name__)
import routes

app.secret_key = getenv("SECRET_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://"
# db = SQLAlchemy(app)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]

#     user = db.session.execute(
#         text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
#     if not user:
#         return "Username not found. <a href='/'>Try again</a>"

#     hash_value = user.password
#     if check_password_hash(hash_value, password):
#         session["username"] = username
#         return redirect("/startpage")

#     else:
#         return "Incorrect password. <a href='/'>Try again</a>"


# @app.route("/logout")
# def logout():
#     del session["username"]
#     return redirect("/")


# @app.route("/register", methods=["POST", "GET"])
# def register():
#     if request.method == "GET":
#         return render_template("register.html")

#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         existing_user = db.session.execute(
#             text("SELECT * FROM users WHERE username = :username"), {"username": username}).fetchone()
#         if existing_user:
#             return "Username already exists. <a href='/register'>Try again</a>"
#         hash_value = generate_password_hash(password)
#         try:
#             query = text(
#                 "INSERT INTO users (username, password) VALUES (:username, :password)")
#             db.session.execute(
#                 query, {"username": username, "password": hash_value})
#             db.session.commit()
#         except Exception as e:
#             print(e)
#             return "Registration failed. <a href='/register'>Try again</a>"
#         session["username"] = username
#         return redirect("/")


# @app.route("/startpage")
# def startpage():
#     return render_template("startpage.html")


# @app.route("/form")
# def form():
#     return render_template("form.html")


# @app.route("/result", methods=["POST"])
# def result():

#     name = request.form["name"]
#     status = request.form["status"]
#     grade = request.form["grade"]
#     review = request.form["review"]

#     username = session['username']
#     query_user = text("SELECT * FROM users WHERE username = :username")
#     result_user = db.session.execute(query_user, {"username": username})
#     user = result_user.fetchone()

#     if not user:
#         return "User not found."

#     try:
#         query = text(
#             "INSERT INTO reviews (user_id, name, status, grade, review) VALUES (:user_id, :name, :status, :grade, :review)")
#         db.session.execute(query, {"user_id": user.id, "name": name,
#                            "status": status, "grade": grade, "review": review})
#         db.session.commit()

#         return render_template("result.html", name=name, status=status, grade=grade, review=review)

#     except Exception as e:
#         print(e)
#         return "Insertion failed. <a href='/form'>Try again</a>"


# @app.route("/search")
# def search():
#     return render_template("search.html")


# @app.route("/myreviews")
# def myreviews():
#     user_reviews = get_user_reviews()

#     if isinstance(user_reviews, str):
#         return render_template("myreviews.html", error_message=user_reviews)

#     return render_template("myreviews.html", user_reviews=user_reviews)


# def get_user_reviews():
#     if 'username' not in session:
#         return "User not logged in."

#     username = session['username']

#     query_user = text("SELECT * FROM users WHERE username = :username")
#     result_user = db.session.execute(query_user, {"username": username})
#     user = result_user.fetchone()

#     if not user:
#         return "User not found."

#     query_reviews = text("SELECT * FROM reviews WHERE user_id = :user_id")
#     result_reviews = db.session.execute(query_reviews, {"user_id": user.id})
#     user_reviews = result_reviews.fetchall()

#     if not user_reviews:
#         return "No reviews found."

#     return user_reviews
