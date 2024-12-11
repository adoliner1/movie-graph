import sys
import os
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

if __name__ == "__main__":
    tmdb = TMDBClient()
    
    # Get Fight Club as an example
    movie_data = tmdb.get_movie(550)
    
    print("Available movie fields:")
    for key in sorted(movie_data.keys()):
        print(f"{key}: {type(movie_data[key]).__name__}")
        
    print("\nExample values for Fight Club:")
    pprint(movie_data)