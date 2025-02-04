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

@app.route('/')
def home():
    return render_template('Start-Screen.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter((User.username == username)).first()
        if existing_user:
            flash('Username or email already exists!', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('Register-Screen.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')

            # Initialize user's movie cache
            user_movie_caches[user.id] = {
                "cache": [],
                "current_page": user.last_page
            }
            
            return redirect(url_for('main'))
        else:
            flash('Login failed. Please check email and password.', 'danger')
    return render_template('Login-Screen.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    global user_movie_caches

    user_id = current_user.id

    if user_id not in user_movie_caches:
        user_movie_caches[user_id] = {
            "cache": [],
            "current_page": current_user.last_page
        }
if not user_movie_caches[user_id]["cache"]:
        fetch_movies()

    return render_template('Movie-Screen.html', user_id=current_user.id)

@app.route('/fetch_movies', methods=['GET'])
def fetch_movies():
    user_id = current_user.id
    user_cache = user_movie_caches.setdefault(user_id, {"cache": [], "current_page": current_user.last_page or 1})

    refresh = request.args.get('refresh', default="false").lower() == "true"

    if refresh:
        user_cache["current_page"] += 1
        if user_cache["current_page"] > 500: 
            user_cache["current_page"] = 1
    else:
        page = request.args.get('page', default=user_cache["current_page"], type=int)
        user_cache["current_page"] = page

    user_cache["cache"] = tmdb.fetch_movie_page(page=user_cache["current_page"])

    current_user.last_page = user_cache["current_page"]
    db.session.commit()

    return jsonify({
        "message": f"Movies fetched successfully for page {user_cache['current_page']}",
        "count": len(user_cache["cache"])
    })

@app.route('/get_movie', methods=['GET'])
@login_required
def get_movie():
    user_id = current_user.id
    user_cache = user_movie_caches.setdefault(user_id, {"cache": [], "current_page": current_user.last_page})

    if not user_cache["cache"]:
        user_cache["current_page"] += 1
        if user_cache["current_page"] > 500:
            user_cache["current_page"] = 1

        user_cache["cache"] = tmdb.fetch_movie_page(page=user_cache["current_page"])

        if not user_cache["cache"]:
            return jsonify({"error": "No movies available even after refetching!"}), 404

    movie = user_cache["cache"].pop()
    movie_details = tmdb.fetch_movie_details(movie["id"])

    runtime = movie_details.get("runtime", "N/A")
    genres = [genre["name"] for genre in movie_details.get("genres", [])]

    return jsonify({
        "id": movie["id"],
        "title": movie["original_title"],
        "rating": movie["vote_average"],
        "duration": runtime,
        "genres": genres,
        "release_date": movie["release_date"],
        "poster_path": movie.get("poster_path", "")
    })
