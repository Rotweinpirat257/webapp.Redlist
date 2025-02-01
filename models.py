from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    last_page = db.Column(db.Integer, default=1)
    groups = db.relationship('Group', secondary='user_groups', back_populates='users')

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, unique=True, nullable=False)  # TMDb movie ID
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # like  dislike
