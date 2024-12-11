import os
from dotenv import load_dotenv

load_dotenv()

def get_neo4j_uri():
    """Ensure Neo4j URI has proper protocol prefix."""
    uri = os.getenv('NEO4J_URI', 'c79bb620.databases.neo4j.io:7687')
    
    # If URI already has a protocol, return as is
    if '://' in uri:
        return uri
        
    # Otherwise, add neo4j+s:// protocol
    return f"neo4j+s://{uri}"

class Config:
    # TMDB Configuration
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    
    # Neo4j Configuration
    NEO4J_URI = get_neo4j_uri()
    NEO4J_USER = os.getenv('NEO4J_USER', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
    
    # Application Settings
    ACTORS_PER_MOVIE = 5  # Number of top-billed actors to include per movie
    MIN_VOTE_COUNT = 1000  # Minimum number of votes for a movie to be included
    MOVIES_PER_PAGE = 20   # TMDB's fixed page size