"""

application.py
Web application for listening and rating albums. 

Minor programmeren 
Web app studio 
Shewen Davelaar

"""


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
    # Get atrists of an album
    list = []
    for item in dict["artists"]:
        list.append(item['name'])
    return str(list).strip('[]')


# The index page of the website
@app.route("/")
def index():
    return render_template("index.html")


#  Log user in using Flask-Spotify-Auth
@app.route("/login")
def login():
    response = getUser()
    return redirect(response)

# Return log for spotify autentication
@app.route("/callback/")
def callback():

    # Use user token
    getUserToken(request.args['code'])

    # Initialize spotipy library using token
    session['spotify'] = spotipy.Spotify(getAccessToken())

    # Return user information
    returned_user = session['spotify'].current_user()
    user = User.query.filter(User.username == returned_user["id"]).first()

    # Add user infomation to database
    if not user:
        userin = User(username=returned_user["id"], display_name=returned_user["display_name"],
                      email=returned_user["email"])
        db.session.add(userin)
        db.session.commit()

        # Return user information
        user = User.query.filter(User.username == returned_user["id"]).first()

    # Log in user
    session["user"] = user

    return redirect(url_for("search"))

# Search for an album
@app.route("/search")
def search():
    if "user" in session:
        return render_template("search.html")
    return redirect(url_for("index"))

# Use the user input to search for album
@app.route("/result", methods=["GET", "POST"])
def result():
    if "user" in session:

        # Search for results
        results = session['spotify'].search(q=request.form.get(
            "userinput"), type="album", market="NL")

        result_list = []

        # Loop through search results
        for album in results["albums"]["items"]:
            albumdict = {}

            # Return artist of the selected album
            albumdict["artist"] = get_artists(album).replace("'", "")

            # Truncate name if name too long
            albumdict["name"] = (album["name"][:40].strip() +
                                 '...') if len(album["name"]) > 40 else album["name"]

            # Add songid
            albumdict["id"] = album["id"]

            # Add song image
            albumdict["image"] = album["images"][2]["url"]

            # Return album
            result_list.append(albumdict)

        return render_template("result.html", result_list=result_list)
    return redirect(url_for("index"))

# Return track information within an album`
@app.route("/album", methods=["POST"])
def album():
    if "user" in session:

        # Return albuminformation
        album = session['spotify'].album(request.form.get("itemid"))

        albumdict = {}

        # Add album inforamtion in albumdict
        albumdict["name"] = album["name"]
        albumdict["date"] = album["release_date"]
        albumdict["total_tracks"] = album["total_tracks"]
        albumdict["images"] = album["images"][1]["url"]
        albumdict["id"] = album["id"]

        albumdict["artist"] = get_artists(album).replace("'", "")

        tracks = []

        # Loop through album tracks
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

# Return information about a song
@app.route("/get_song", methods=["POST"])
def get_song():

    # Request song information at the spotify api using Spotipy
    song = session['spotify'].track(request.form.get("songid"))

    # Return song information in json form
    return jsonify({"name": song["name"], "uri": song["uri"], "artist": song["artists"]
                    [0]["name"], "image": song["album"]["images"][2]["url"]})

# Return a fresh Spotify autentication token using Flask-Spotify-Auth
@app.route("/get_token", methods=["POST"])
def get_token():

    return jsonify({"token": getAccessToken()})

# MAke and return user reviews
@app.route("/review", methods=["POST"])
def review():

    # Query albums in album table
    if not Album.query.filter(Album.album_code == session["album"]["id"]).first():
        add_album = Album(album_code=session["album"]["id"], artists=session["album"]["artist"],
                          name=session["album"]["name"], image=session["album"]["images"])
        db.session.add(add_album)
        db.session.commit()

    # Return album
    album = Album.query.filter(
        Album.album_code == session["album"]["id"]).first()

    # Check if review already in database
    if not Review.query.filter(and_(Review.album_id == album.id, Review.user_id == session['user'].id)).first():

        # Add new review to database
        list = request.form.getlist("albumtracks")

        # Calculate review
        number = float(10/(len(list)*5))
        avg = float(number * sum([int(cijfer) for cijfer in list]))

        # Add review to database
        review = Review(user_id=session['user'].id,
                        album_id=album.id, rating=avg)
        db.session.add(review)
        db.session.commit()

    # Return user profile page
    return redirect(url_for("profile"))

# Load user profile page
@app.route("/profile")
def profile():
    if "user" in session:

        # Query reviews made by user
        reviewed_albums = db.session.query(Review, Album).filter(
            and_(Review.album_id == Album.id, Review.user_id == session['user'].id)).all()

        # Return albums reviewed by user
        return render_template("profile.html", reviews=reviewed_albums)
    return redirect(url_for("index"))

# Log out user
@app.route("/logout")
def logout():

    # Remove user from session
    session.pop("user", None)

    # Spotify logout page
    return redirect("https://www.spotify.com/logout/")
