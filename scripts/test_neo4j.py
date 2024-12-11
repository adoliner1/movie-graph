import sys
import os
from neo4j import GraphDatabase

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def test_connection():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Simple query to verify connection
            result = session.run("RETURN 1 AS test")
            record = result.single()
            print("Connection successful!")
            print(f"Test query result: {record['test']}")
    except Exception as e:
        print(f"Connection failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    print(f"Using credentials from .env file...")
    print(f"Username: {Config.NEO4J_USER}")
    print(f"Password: {'*' * len(Config.NEO4J_PASSWORD) if Config.NEO4J_PASSWORD else 'Not set!'}")
    print(f"\nTesting connection...")
    test_connection()