import pytest
from src.neo4j_client import Neo4jClient

def test_neo4j_client_initialization():
    client = Neo4jClient(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    assert client.uri == "bolt://localhost:7687"
    assert client.user == "neo4j"
    assert client.password == "password"
    assert client.driver is None

# Add more tests here as needed