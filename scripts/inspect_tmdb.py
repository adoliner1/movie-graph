import sys
import os
import json
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

if __name__ == "__main__":
    tmdb = TMDBClient()
    
    # Get basic movie data
    movie_data = tmdb.get_movie(550)  # Fight Club
    print("\nBASIC MOVIE DATA STRUCTURE:")
    pprint(movie_data)

    # Get credits data (separate endpoint we need to add)
    try:
        credits_data = tmdb._make_request(f"/movie/550/credits")
        print("\nCREDITS DATA STRUCTURE:")
        pprint(credits_data)
    except Exception as e:
        print(f"Error getting credits: {e}")
