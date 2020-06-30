import os
from flask import Flask, render_template, request, url_for, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy, inspect, sqlalchemy
from sqlalchemy import and_
from flask_migrate import Migrate
from models import *


# Configure Flask appz
app = Flask(__name__)

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
db.init_app(app)

# Configure session, use filesystem
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure migrations
Migrate(app, db)

# The index page of the website
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/result")
def result():
    return render_template("result.html")
