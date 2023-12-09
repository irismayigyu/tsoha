
from os import getenv
from flask import Flask
from flask import flash

app = Flask(__name__)
import routes
app.secret_key = getenv("SECRET_KEY")
