import os
from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import and_
from flask_migrate import Migrate
from .models import *
from .spotify.startup import *
import spotipy


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


def get_artists(dict):
    list = []
    for item in dict["artists"]:
        list.append(item['name'])
    return str(list).strip('[]')


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
    return render_template("search.html")


@app.route("/result", methods=["GET", "POST"])
def result():

    session['spotify'] = spotipy.Spotify(getAccessToken())
    results = session['spotify'].search(q=request.form.get(
        "userinput"), type="album", market="NL")

    result_list = []
    for album in results["albums"]["items"]:
        albumdict = {}
        artistlist = []

        albumdict["artist"] = get_artists(album)
        albumdict["name"] = album["name"]
        albumdict["id"] = album["id"]
        albumdict["image"] = album["images"][2]["url"]
        result_list.append(albumdict)

    return render_template("result.html", result_list=result_list)


@app.route("/album", methods=["POST"])
def album():

    tracks = []
    artistlist = []
    albumdict = {}

    album = session['spotify'].album(request.form.get("itemid"))
    albumdict["name"] = album["name"]
    albumdict["date"] = album["release_date"]
    albumdict["total_tracks"] = album["total_tracks"]
    albumdict["images"] = album["images"][1]["url"]
    albumdict["id"] = album["id"]

    albumdict["artist"] = get_artists(album)

    for track in album["tracks"]["items"]:
        trackdict = {}
        trackdict["name"] = track["name"]
        trackdict["id"] = track["id"]
        trackdict["uri"] = track["uri"]
        tracks.append(trackdict)
    albumdict["tracks"] = tracks
    return albumdict


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/get_song", methods=["POST"])
def get_song():
    print(getAccessToken())
    song = session['spotify'].track(request.form.get("songid"))
    object = jsonify({"name": song["name"], "uri": song["uri"], "artist": song["artists"]
                      [0]["name"], "image": song["album"]["images"][2]["url"]})
    return object


@app.route("/get_token", methods=["POST"])
def get_token():
    return jsonify({"token": getAccessToken()})


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/play_song")
def play_song():
    session['spotify'].start_play(device_id=request.form.get(
        "player"), context_uri=request.form.get("uri"))
    return jsonify({"success": True})
