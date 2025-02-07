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


@app.route('/action', methods=['POST'])
def action():
    data = request.json
    user_id = data.get('user_id')
    movie_id = data.get('movie_id')
    status = data.get('status')  

    existing_match = Matches.query.filter_by(user_id=user_id, movie_id=movie_id).first()

    if existing_match:
        existing_match.status = status
    else:
        new_match = Matches(user_id=user_id, movie_id=movie_id, status=status)
        db.session.add(new_match)

    other_likes = Matches.query.filter(Matches.movie_id == movie_id, Matches.status == 'like', Matches.user_id != user_id).count()

    if other_likes > 0 and status == 'like':
        message = "Another user also likes this movie!"
    else:
        message = f"Movie {status} recorded successfully"

    db.session.commit()
    return jsonify({"message": message})

@app.route('/matches', methods=['GET'])
@login_required
def liked_movies():
    user_id = current_user.id

    current_user_likes = (
        db.session.query(
            Matches.movie_id
        )
        .filter(Matches.user_id == user_id, Matches.status == 'like')
        .distinct()
        .all()
    )

    liked_movie_ids = [movie_id for (movie_id,) in current_user_likes]

    movie_like_counts = (
        db.session.query(
            Matches.movie_id,
            func.count(Matches.user_id).label('total_likes')
        )
        .filter(Matches.movie_id.in_(liked_movie_ids), Matches.status == 'like')
        .group_by(Matches.movie_id)
        .all()
    )

    # Build a response with movie details and like counts
    movies_data = []
    for movie_id, total_likes in movie_like_counts:
        others_likes = total_likes - 1 if total_likes > 1 else 0

        movie_details = tmdb.fetch_movie_details(movie_id)  
        movies_data.append({
            "id": movie_id,
            "title": movie_details.get('title', 'Unknown'),
            "poster_path": movie_details.get('poster_path', ''),
            "others_likes": others_likes
        })

    return render_template('Match-Screen.html', movies=movies_data)



@app.route('/movie/<int:movie_id>/likes', methods=['GET'])
@login_required
def movie_likes(movie_id):
    movie = tmdb.fetch_movie_details(movie_id)  

    liked_users = Matches.query.filter_by(movie_id=movie_id, status='like').all()
    users_data = []
    for match in liked_users:
        if match.user_id == current_user.id:
            continue

        user = User.query.get(match.user_id)
        if user:
            users_data.append({
                "username": user.username,
                "user_id": user.id
            })
    return render_template('Likes-Screen.html', movie=movie, users=users_data)

@app.route('/groups')
@login_required
def my_groups():
    current_username = current_user.username

    groups = current_user.groups
    for group in groups:
        name_1 = group.name.split("_")[0]
        name_2 = group.name.split("_")[1]
