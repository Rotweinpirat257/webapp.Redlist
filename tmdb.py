import random
import requests

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNDQ1ZGVjMzNjMTIxNjIzODMxYzM1ZWRjOTAwYzZhZCIsIm5iZiI6MTczNjg2NzE5NC4xMjcsInN1YiI6IjY3ODY3ZDdhMjI1NjAyM2RmZDRlOTc1NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ._sKOX_egvO0vPr0rB4ArGv0sKbMb78sqf8wiTK0KCk4"

def fetch_movie_page(page=1):
    """Fetch a specific page of movies from the TMDb API."""
    base_url = f"https://api.themoviedb.org/3/discover/movie"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + API_KEY
    }

    params = {
        "include_adult": False,
        "include_video": False,
        "language": "en-US",
        "page": page,
        "sort_by": "popularity.desc"
    }

    response = requests.get(base_url, headers=headers, params=params)
    data = response.json()

    if "results" in data:
        movies = data["results"]
        return movies
    else:
        return []


def fetch_movie_details(movie_id):
    api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {}

if __name__ == "__main__":
    movie = fetch_movie_page()
    if movie:
        print(f"Random Movie: {movie['title']} ({movie['release_date']})")
    else:
        print("No movies found!")


