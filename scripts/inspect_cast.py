import sys
import os
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

if __name__ == "__main__":
    tmdb = TMDBClient()
    
    credits_data = tmdb._make_request(f"/movie/550/credits")
    
    # Get just the top 5 actors
    print("\nTOP 5 ACTORS:")
    top_actors = credits_data['cast'][:5]
    pprint(top_actors)
    
    # Get just the director(s)
    print("\nDIRECTOR(S):")
    directors = [crew for crew in credits_data['crew'] if crew['job'] == 'Director']
    pprint(directors)