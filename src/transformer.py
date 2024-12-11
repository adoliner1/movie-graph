from typing import Dict, List, Set
from .config import Config
from .tmdb_client import TMDBClient
from .models.models import MovieNode, PersonNode, Relationship

class TMDBTransformer:
    def __init__(self, tmdb_client: TMDBClient = None):
        self.tmdb = tmdb_client or TMDBClient()
        self.movies: Dict[int, MovieNode] = {}
        self.people: Dict[int, PersonNode] = {}
        self.relationships: Set[Relationship] = set()

    def transform_movie_data(self, movie_data: dict) -> MovieNode:
        """Transform raw TMDB movie data into a MovieNode."""
        genres = [genre['name'] for genre in movie_data.get('genres', [])]
        
        return MovieNode(
            id=movie_data['id'],
            title=movie_data['title'],
            release_date=movie_data['release_date'],
            overview=movie_data['overview'],
            tagline=movie_data.get('tagline', ''),
            genres=genres
        )

    def transform_person_data(self, person_data: dict) -> PersonNode:
        """Transform raw TMDB person data into a PersonNode."""
        return PersonNode(
            id=person_data['id'],
            name=person_data['name'],
            profile_path=person_data.get('profile_path'),
            popularity=person_data.get('popularity', 0.0)
        )

    def process_movie(self, movie_id: int) -> None:
        """Process a single movie and its associated people."""
        # Get basic movie data
        movie_data = self.tmdb.get_movie(movie_id)
        
        # Create movie node if we don't have it
        if movie_id not in self.movies:
            self.movies[movie_id] = self.transform_movie_data(movie_data)

        # Get credits data
        credits_data = self.tmdb._make_request(f"/movie/{movie_id}/credits")

        # Process top-billed actors
        for actor in credits_data['cast'][:Config.ACTORS_PER_MOVIE]:
            # Create person node if we don't have them
            if actor['id'] not in self.people:
                self.people[actor['id']] = self.transform_person_data(actor)
            
            # Create ACTED_IN relationship
            self.relationships.add(Relationship(
                person_id=actor['id'],
                movie_id=movie_id,
                type='ACTED_IN',
                character=actor['character'],
                order=actor['order']
            ))

        # Process directors
        directors = [c for c in credits_data['crew'] if c['job'] == 'Director']
        for director in directors:
            # Create person node if we don't have them
            if director['id'] not in self.people:
                self.people[director['id']] = self.transform_person_data(director)
            
            # Create DIRECTED relationship
            self.relationships.add(Relationship(
                person_id=director['id'],
                movie_id=movie_id,
                type='DIRECTED'
            ))

    def process_movies(self, movie_ids: List[int]) -> None:
        """Process multiple movies."""
        for movie_id in movie_ids:
            self.process_movie(movie_id)

    def fetch_popular_movies(self, start_page: int = 1, num_pages: int = 1) -> List[int]:
        """Fetch popular movies sorted by vote average."""
        movie_ids = []
        
        for page in range(start_page, start_page + num_pages):
            response = self.tmdb._make_request("/discover/movie", {
                'sort_by': 'vote_average.desc',
                'page': page,
                'vote_count.gte': Config.MIN_VOTE_COUNT,
                'include_adult': False
            })
            
            for movie in response['results']:
                movie_ids.append(movie['id'])

        return movie_ids

    def get_stats(self) -> Dict:
        """Get statistics about the processed data."""
        return {
            'movies': len(self.movies),
            'people': len(self.people),
            'relationships': len(self.relationships),
            'actors': len([r for r in self.relationships if r.type == 'ACTED_IN']),
            'directors': len([r for r in self.relationships if r.type == 'DIRECTED'])
        }