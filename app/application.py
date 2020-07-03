import os
from flask import Flask, render_template, request, url_for, session, redirect
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import and_
from flask_migrate import Migrate
from .models import *
from .spotify.startup import *

# Configure Flask appz
app = Flask(__name__)

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
db.init_app(app)

# Configure session, use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure migrationsea
Migrate(app, db)

# The index page of the website
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    response = getUser()
    return redirect(response)


@app.route("/callback/")
def callback():
    getUserToken(request.args['code'])
    return redirect(url_for("search"))


@app.route("/search")
def search():
    print(getAccessToken())
    return render_template("search.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/album")
def album():
    return render_template("album.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/about")
def about():
    return render_template("about.html")
