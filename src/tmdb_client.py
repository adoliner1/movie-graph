import requests
from .config import Config

class TMDBClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.TMDB_API_KEY
        self.base_url = Config.TMDB_BASE_URL

    def _make_request(self, endpoint, params=None):
        """Make a request to TMDB API with proper error handling"""
        params = params or {}
        params['api_key'] = self.api_key
        
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_movie(self, movie_id):
        """Get detailed information about a movie"""
        return self._make_request(f"/movie/{movie_id}")

    def get_person(self, person_id):
        """Get detailed information about a person"""
        return self._make_request(f"/person/{person_id}")

    def search_movies(self, query, page=1):
        """Search for movies by title"""
        return self._make_request("/search/movie", {
            'query': query,
            'page': page
        })