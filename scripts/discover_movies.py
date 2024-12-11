import sys
import os
from typing import Dict, List, Set
from dataclasses import dataclass
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient
from scripts.import_to_neo4j import import_movies_to_neo4j

def get_popular_movies(tmdb_client: TMDBClient, num_pages: int = 1) -> List[int]:
    """
    Fetch popular movies sorted by popularity.
    Each page contains 20 movies.
    """
    movie_ids = []
    
    for page in range(1, num_pages + 1):
        # Use the discover endpoint to get movies sorted by popularity
        response = tmdb_client._make_request("/discover/movie", {
            'sort_by': 'popularity.desc',
            'page': page,
            'include_adult': False,
            'vote_count.gte': 100  # Only get movies with at least 100 votes
        })
        
        # Extract movie IDs
        for movie in response['results']:
            movie_ids.append(movie['id'])
            
        print(f"Fetched page {page}/{num_pages} - Total movies so far: {len(movie_ids)}")
    
    return movie_ids

if __name__ == "__main__":
    # How many pages to fetch (20 movies per page)
    PAGES_TO_FETCH = 5  # This will get 100 movies
    
    # First clear the database
    print("Note: Make sure to run clear_neo4j.py first if you want to start fresh!")
    input("Press Enter to continue...")
    
    # Get popular movie IDs
    print(f"\nFetching {PAGES_TO_FETCH} pages of popular movies...")
    tmdb = TMDBClient()
    movie_ids = get_popular_movies(tmdb, num_pages=PAGES_TO_FETCH)
    
    print(f"\nFound {len(movie_ids)} movies")
    print("\nExample movies (first 5):")
    for movie_id in movie_ids[:5]:
        movie = tmdb.get_movie(movie_id)
        print(f"ID: {movie_id}, Title: {movie['title']}, Popularity: {movie['popularity']}")
    
    print("\nProceeding to import these movies to Neo4j...")
    import_movies_to_neo4j(movie_ids)