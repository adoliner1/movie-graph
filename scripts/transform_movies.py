import sys
import os
from typing import Dict, List, Set
from dataclasses import dataclass
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.tmdb_client import TMDBClient

@dataclass
class MovieNode:
    id: int
    title: str
    release_date: str
    overview: str
    tagline: str
    genres: List[str]  # List of genre names

@dataclass
class PersonNode:
    id: int
    name: str
    profile_path: str
    popularity: float

@dataclass(frozen=True)
class Relationship:
    person_id: int
    movie_id: int
    type: str
    character: str = ''
    order: int = -1

class TMDBTransformer:
    def __init__(self):
        self.tmdb = TMDBClient()
        self.movies: Dict[int, MovieNode] = {}
        self.people: Dict[int, PersonNode] = {}
        self.relationships: Set[Relationship] = set()

    def process_movie(self, movie_id: int):
        """Fetch and process a single movie and its credits"""
        # Get basic movie data
        movie_data = self.tmdb.get_movie(movie_id)
        
        # Extract genre names
        genres = [genre['name'] for genre in movie_data.get('genres', [])]
        
        # Create movie node if we don't have it
        if movie_id not in self.movies:
            self.movies[movie_id] = MovieNode(
                id=movie_id,
                title=movie_data['title'],
                release_date=movie_data['release_date'],
                overview=movie_data['overview'],
                tagline=movie_data.get('tagline', ''),  # Use empty string if no tagline
                genres=genres
            )

        # Get credits data
        credits_data = self.tmdb._make_request(f"/movie/{movie_id}/credits")

        # Process cast (top 5 actors)
        for actor in credits_data['cast'][:5]:
            # Create person node if we don't have them
            if actor['id'] not in self.people:
                self.people[actor['id']] = PersonNode(
                    id=actor['id'],
                    name=actor['name'],
                    profile_path=actor['profile_path'],
                    popularity=actor['popularity']
                )
            
            # Add relationship to set
            self.relationships.add(Relationship(
                person_id=actor['id'],
                movie_id=movie_id,
                type='ACTED_IN',
                character=actor['character'],
                order=actor['order']
            ))

        # Process director
        directors = [c for c in credits_data['crew'] if c['job'] == 'Director']
        for director in directors:
            # Create person node if we don't have them
            if director['id'] not in self.people:
                self.people[director['id']] = PersonNode(
                    id=director['id'],
                    name=director['name'],
                    profile_path=director['profile_path'],
                    popularity=director['popularity']
                )
            
            # Add relationship to set
            self.relationships.add(Relationship(
                person_id=director['id'],
                movie_id=movie_id,
                type='DIRECTED'
            ))

    def print_summary(self):
        """Print a summary of all nodes and relationships"""
        print("\nMOVIES:")
        for movie in sorted(self.movies.values(), key=lambda x: x.title):
            print(f"- {movie.title} (ID: {movie.id})")
            print(f"  Genres: {', '.join(movie.genres)}")
            if movie.tagline:
                print(f"  Tagline: {movie.tagline}")
        
        print("\nPEOPLE:")
        for person in sorted(self.people.values(), key=lambda x: x.name):
            print(f"- {person.name} (ID: {person.id})")
        
        print("\nRELATIONSHIPS:")
        sorted_relationships = sorted(
            self.relationships,
            key=lambda x: (
                self.movies[x.movie_id].title,
                x.type,
                x.order if x.type == 'ACTED_IN' else -1
            )
        )
        
        for rel in sorted_relationships:
            person_name = self.people[rel.person_id].name
            movie_title = self.movies[rel.movie_id].title
            if rel.type == 'ACTED_IN':
                print(f"- {person_name} played {rel.character} in {movie_title}")
            else:
                print(f"- {person_name} directed {movie_title}")

if __name__ == "__main__":
    # List of movie IDs to process
    movie_ids = [
        550,    # Fight Club
        807,    # Se7en
        37799,  # The Social Network
        210577  # Gone Girl
    ]
    
    transformer = TMDBTransformer()
    
    # Process each movie
    for movie_id in movie_ids:
        print(f"Processing movie ID: {movie_id}")
        transformer.process_movie(movie_id)
    
    # Print summary
    transformer.print_summary()