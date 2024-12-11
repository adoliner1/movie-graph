import sys
import os
from typing import Dict, List, Set
from dataclasses import dataclass
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient
from scripts.import_to_neo4j import import_movies_to_neo4j

def get_next_top_rated_movies(tmdb_client: TMDBClient, start_page: int = 14, num_pages: int = 13) -> List[int]:
    """
    Fetch the next batch of top rated movies.
    """
    movie_ids = []
    min_votes = 1000  # Requiring at least 1000 votes
    
    for page in range(start_page, start_page + num_pages):
        # Use the discover endpoint to get movies sorted by rating
        response = tmdb_client._make_request("/discover/movie", {
            'sort_by': 'vote_average.desc',
            'page': page,
            'vote_count.gte': min_votes,  # Minimum vote threshold
            'include_adult': False
        })
        
        # Extract movie IDs and their ratings
        for movie in response['results']:
            movie_ids.append(movie['id'])
            
        print(f"Fetched page {page} - Total movies so far: {len(movie_ids)}")
    
    return movie_ids[:250]  # Ensure we only get 250 movies

if __name__ == "__main__":
    print("This script will fetch movies ranked 251-500 from TMDB")
    print("Note: These will be added to the existing database!")
    input("Press Enter to continue...")
    
    # Get next batch of top rated movie IDs
    print("\nFetching next 250 top rated movies...")
    tmdb = TMDBClient()
    movie_ids = get_next_top_rated_movies(tmdb)
    
    print(f"\nFound {len(movie_ids)} movies")
    print("\nExample movies (first 10):")
    for movie_id in movie_ids[:10]:
        movie = tmdb.get_movie(movie_id)
        print(f"Title: {movie['title']:<50} Rating: {movie['vote_average']} ({movie['vote_count']} votes)")
    
    proceed = input("\nWould you like to import these additional movies to Neo4j? (yes/no): ")
    if proceed.lower() == 'yes':
        print("\nProceeding to import these movies to Neo4j...")
        import_movies_to_neo4j(movie_ids)
    else:
        print("Import cancelled.")