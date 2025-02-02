from flask import Flask, render_template,request, redirect, url_for, flash, jsonify, session
from sqlalchemy import func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Matches, Group, Message
import tmdb

user_movie_caches = {}  # {user_id: {"cache": [], "current_page": int}}

current_page = 1

class Config:
    SECRET_KEY = 'red_list'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)
