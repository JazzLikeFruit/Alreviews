import os
from flask import Flask, render_template, request, url_for, session, redirect, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy import and_
from flask_migrate import Migrate
from .models import *
from .spotify.startup import *
import spotipy


# Configure Flask apps
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
    session['spotify'] = spotipy.Spotify(getAccessToken())
    returned_user = session['spotify'].current_user()
    user = User.query.filter(User.username == returned_user["id"]).first()

    if not user:
        userin = User(username=returned_user["id"], display_name=returned_user["display_name"],
                      email=returned_user["email"])
        db.session.add(userin)
        db.session.commit()

        user = User.query.filter(User.username == returned_user["id"]).first()

    # Log in user
    session["user"] = user

    return redirect(url_for("search"))


@app.route("/search")
def search():
    if "user" in session:
        print(session["user"])
        return render_template("search.html")
    return redirect(url_for("index"))


@app.route("/result", methods=["GET", "POST"])
def result():
    if "user" in session:
        results = session['spotify'].search(q=request.form.get(
            "userinput"), type="album", market="NL")

        result_list = []
        for album in results["albums"]["items"]:
            albumdict = {}
            artistlist = []

            albumdict["artist"] = get_artists(album).replace("'", "")
            albumdict["name"] = album["name"]
            albumdict["id"] = album["id"]
            albumdict["image"] = album["images"][2]["url"]
            result_list.append(albumdict)

        return render_template("result.html", result_list=result_list)
    return redirect(url_for("index"))


@app.route("/album", methods=["POST"])
def album():
    if "user" in session:
        tracks = []
        artistlist = []
        albumdict = {}

        album = session['spotify'].album(request.form.get("itemid"))
        albumdict["name"] = album["name"]
        albumdict["date"] = album["release_date"]
        albumdict["total_tracks"] = album["total_tracks"]
        albumdict["images"] = album["images"][1]["url"]
        albumdict["id"] = album["id"]

        albumdict["artist"] = get_artists(album).replace("'", "")

        for track in album["tracks"]["items"]:
            trackdict = {}
            trackdict["name"] = track["name"]
            trackdict["id"] = track["id"]
            trackdict["uri"] = track["uri"]
            tracks.append(trackdict)
        albumdict["tracks"] = tracks
        session["album"] = albumdict
        return albumdict
    return redirect(url_for("index"))


@app.route("/get_song", methods=["POST"])
def get_song():

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


@app.route("/review", methods=["POST"])
def review():

    if not Album.query.filter(Album.album_code == session["album"]["id"]).first():
        add_album = Album(album_code=session["album"]["id"], artists=session["album"]["artist"],
                          name=session["album"]["name"], image=session["album"]["images"])
        db.session.add(add_album)
        db.session.commit()

    album = Album.query.filter(
        Album.album_code == session["album"]["id"]).first()

    if not Review.query.filter(and_(Review.album_id == album.id, Review.user_id == session['user'].id)).first():

        list = request.form.getlist("albumtracks")
        avg = sum([int(cijfer) for cijfer in list]) / len(list)

        review = Review(user_id=session['user'].id,
                        album_id=album.id, rating=avg)
        db.session.add(review)
        db.session.commit()
    return redirect(url_for("profile"))


@app.route("/profile")
def profile():
    if "user" in session:
        reviews = Review.query.filter(
            Review.user_id == session['user'].id).all()

        return render_template("profile.html", reviews=reviews)
    return redirect(url_for("index"))

# Log out user
@app.route("/logout")
def logout():

    session.pop("user", None)

    # spotify logout page
    return redirect("https://www.spotify.com/logout/")
