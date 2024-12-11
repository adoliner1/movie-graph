import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

print("Python path:", sys.path)
print("Current working directory:", os.getcwd())
print("Project root added:", project_root)

from src.tmdb_client import TMDBClient
from src.neo4j_client import Neo4jClient

def import_movie(movie_id):
    """Import a single movie and its relationships"""
    tmdb = TMDBClient()
    neo4j = Neo4jClient()
    
    try:
        # Get movie data from TMDB
        movie_data = tmdb.get_movie(movie_id)
        
        # Connect to Neo4j
        neo4j.connect()
        
        # Create movie node
        neo4j.create_movie(movie_data)
        
        print(f"Successfully imported movie: {movie_data['title']}")
        
    except Exception as e:
        print(f"Error importing movie {movie_id}: {str(e)}")
    
    finally:
        neo4j.close()

if __name__ == "__main__":
    # Example usage
    import_movie(550)  # Fight Club