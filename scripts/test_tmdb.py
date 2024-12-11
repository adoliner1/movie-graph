import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

if __name__ == "__main__":
    tmdb = TMDBClient()
    try:
        # Try to get Fight Club's data
        movie_data = tmdb.get_movie(550)
        print("Successfully retrieved movie data:")
        print(f"Title: {movie_data['title']}")
        print(f"Release Date: {movie_data['release_date']}")
        print(f"Overview: {movie_data['overview'][:100]}...")  # Just first 100 chars of overview
    except Exception as e:
        print(f"Error: {str(e)}")