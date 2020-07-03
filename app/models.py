from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    Model for every user of the app. 

    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    reviews = db.relationship("Album",
                              secondary="review", lazy="dynamic")


class Review(db.Model):
    """
    Model for reviewed albums by users
    """
    __tablename__ = 'review'
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey(
        'album.id'), primary_key=True)
    rating = db.Column(db.Float, nullable=True)


class Album(db.Model):
    """
    Model for all used albums in the app 

    """
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True)
    artists = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    genres = db.Column(db.String, nullable=False)
    album_type = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
