#!/usr/bin/env python3
import argparse
from src.tmdb_client import TMDBClient
from src.neo4j_client import Neo4jClient
from src.transformer import TMDBTransformer
from src.config import Config

def setup_database(args):
    """Setup/reset Neo4j database constraints."""
    client = Neo4jClient()
    client.setup_constraints()
    print("Database constraints configured successfully.")

def clear_database(args):
    """Clear all data from Neo4j database."""
    client = Neo4jClient()
    client.clear_database()
    print("Database cleared successfully.")

def import_movies(args):
    """Import movies from TMDB to Neo4j."""
    # Initialize components
    transformer = TMDBTransformer()
    neo4j = Neo4jClient()
    
    # Calculate pages needed
    movies_needed = args.count
    pages_needed = (movies_needed + Config.MOVIES_PER_PAGE - 1) // Config.MOVIES_PER_PAGE
    start_page = ((args.start - 1) // Config.MOVIES_PER_PAGE) + 1
    
    print(f"Fetching approximately {movies_needed} movies starting from rank {args.start}...")
    
    # Fetch movie IDs
    movie_ids = transformer.fetch_popular_movies(
        start_page=start_page,
        num_pages=pages_needed
    )[:movies_needed]  # Trim to exact count needed
    
    print(f"Processing {len(movie_ids)} movies...")
    
    # Process movies through transformer
    transformer.process_movies(movie_ids)
    
    # Get stats before import
    stats = transformer.get_stats()
    
    print("\nReady to import:")
    print(f"Movies: {stats['movies']}")
    print(f"People: {stats['people']}")
    print(f"Relationships: {stats['relationships']}")
    print(f"- Acted In: {stats['actors']}")
    print(f"- Directed: {stats['directors']}")
    
    # Confirm before import
    if not args.yes:
        response = input("\nProceed with import? (yes/no): ")
        if response.lower() != 'yes':
            print("Import cancelled.")
            return
    
    print("\nImporting to Neo4j...")
    neo4j.create_graph_objects(
        list(transformer.movies.values()),
        list(transformer.people.values()),
        list(transformer.relationships)
    )
    
    print("Import completed successfully!")

def main():
    parser = argparse.ArgumentParser(description='Movie Graph Database Tool')
    subparsers = parser.add_subparsers(title='commands', required=True)
    
    # Setup database command
    setup_parser = subparsers.add_parser('setup', help='Setup/reset database constraints')
    setup_parser.set_defaults(func=setup_database)
    
    # Clear database command
    clear_parser = subparsers.add_parser('clear', help='Clear all data from database')
    clear_parser.set_defaults(func=clear_database)
    
    # Import movies command
    import_parser = subparsers.add_parser('import', help='Import movies from TMDB')
    import_parser.add_argument(
        '--count', 
        type=int, 
        default=250,
        help='Number of movies to import (default: 250)'
    )
    import_parser.add_argument(
        '--start', 
        type=int, 
        default=1,
        help='Starting rank (default: 1)'
    )
    import_parser.add_argument(
        '--yes', 
        action='store_true',
        help='Skip confirmation prompt'
    )
    import_parser.set_defaults(func=import_movies)
    
    # Parse and execute
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()