import sys
import os
from neo4j import GraphDatabase
from typing import Dict, List, Set

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config
from scripts.transform_movies import TMDBTransformer

class Neo4jImporter:
    def __init__(self):
        self.uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_movie(self, tx, movie):
        query = """
        MERGE (m:Movie {id: $id})
        SET m.title = $title,
            m.release_date = $release_date,
            m.overview = $overview,
            m.tagline = $tagline,
            m.genres = $genres
        """
        tx.run(query, 
            id=movie.id,
            title=movie.title,
            release_date=movie.release_date,
            overview=movie.overview,
            tagline=movie.tagline,
            genres=movie.genres
        )

    def create_person(self, tx, person):
        query = """
        MERGE (p:Person {id: $id})
        SET p.name = $name,
            p.profile_path = $profile_path,
            p.popularity = $popularity
        """
        tx.run(query,
            id=person.id,
            name=person.name,
            profile_path=person.profile_path,
            popularity=person.popularity
        )

    def create_relationship(self, tx, rel):
        if rel.type == 'ACTED_IN':
            query = """
            MATCH (p:Person {id: $person_id})
            MATCH (m:Movie {id: $movie_id})
            MERGE (p)-[r:ACTED_IN {character: $character}]->(m)
            SET r.order = $order
            """
            tx.run(query,
                person_id=rel.person_id,
                movie_id=rel.movie_id,
                character=rel.character,
                order=rel.order
            )
        elif rel.type == 'DIRECTED':
            query = """
            MATCH (p:Person {id: $person_id})
            MATCH (m:Movie {id: $movie_id})
            MERGE (p)-[r:DIRECTED]->(m)
            """
            tx.run(query,
                person_id=rel.person_id,
                movie_id=rel.movie_id
            )

def import_movies_to_neo4j(movie_ids):
    # First, get all data from TMDB
    print("Fetching data from TMDB...")
    transformer = TMDBTransformer()
    for movie_id in movie_ids:
        print(f"Processing movie ID: {movie_id}")
        transformer.process_movie(movie_id)

    # Now import to Neo4j
    print("\nImporting data to Neo4j...")
    importer = Neo4jImporter()
    
    try:
        with importer.driver.session() as session:
            # First create all movies
            print("Creating movie nodes...")
            for movie in transformer.movies.values():
                session.execute_write(importer.create_movie, movie)
            
            # Then create all people
            print("Creating person nodes...")
            for person in transformer.people.values():
                session.execute_write(importer.create_person, person)
            
            # Finally create all relationships
            print("Creating relationships...")
            for rel in transformer.relationships:
                session.execute_write(importer.create_relationship, rel)
                
        print("\nImport completed successfully!")
        
        # Print some stats
        print("\nStats:")
        print(f"Movies created: {len(transformer.movies)}")
        print(f"People created: {len(transformer.people)}")
        print(f"Relationships created: {len(transformer.relationships)}")
        
    finally:
        importer.close()

if __name__ == "__main__":
    # Let's start with our Fincher movies
    movie_ids = [
        550,    # Fight Club
        807,    # Se7en
        37799,  # The Social Network
        210577  # Gone Girl
    ]
    
    import_movies_to_neo4j(movie_ids)