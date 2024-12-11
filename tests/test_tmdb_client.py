import pytest
from src.tmdb_client import TMDBClient

def test_tmdb_client_initialization():
    client = TMDBClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.base_url == "https://api.themoviedb.org/3"

# Add more tests here as needed