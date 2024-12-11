from neo4j import GraphDatabase
from typing import Dict, List
from .config import Config
from .models.models import MovieNode, PersonNode, Relationship

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

    def close(self):
        if self.driver:
            self.driver.close()

    def clear_database(self):
        """Remove all nodes and relationships from the database."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def setup_constraints(self):
        """Set up uniqueness constraints on IDs."""
        with self.driver.session() as session:
            # Drop any existing constraints
            session.run("DROP CONSTRAINT movie_title IF EXISTS")
            session.run("DROP CONSTRAINT person_name IF EXISTS")
            
            # Create ID-based constraints
            session.run("CREATE CONSTRAINT movie_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.id IS UNIQUE")
            session.run("CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")

    def create_movie(self, tx, movie: MovieNode):
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

    def create_person(self, tx, person: PersonNode):
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

    def create_relationship(self, tx, rel: Relationship):
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

    def create_graph_objects(self, movies: List[MovieNode], people: List[PersonNode], relationships: List[Relationship]):
        """Create all nodes and relationships in the database."""
        with self.driver.session() as session:
            # Create all movies
            for movie in movies:
                session.execute_write(self.create_movie, movie)
            
            # Create all people
            for person in people:
                session.execute_write(self.create_person, person)
            
            # Create all relationships
            for rel in relationships:
                session.execute_write(self.create_relationship, rel)