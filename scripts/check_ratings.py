import sys
import os
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

if __name__ == "__main__":
    tmdb = TMDBClient()
    
    # Let's check a few well-known movies
    movie_ids = [
        550,    # Fight Club
        807,    # Se7en
        238,    # The Godfather
        299534  # Avengers: Endgame
    ]
    
    print("Comparing popularity vs vote_average:\n")
    for movie_id in movie_ids:
        movie = tmdb.get_movie(movie_id)
        print(f"Movie: {movie['title']}")
        print(f"popularity: {movie['popularity']}")
        print(f"vote_average: {movie['vote_average']} (from {movie['vote_count']} votes)")
        print("") 