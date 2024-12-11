import sys
import os
from neo4j import GraphDatabase

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def clear_database():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            print("Clearing all nodes and relationships...")
            result = session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared!")
            
            # Verify it's empty
            result = session.run("MATCH (n) RETURN count(n) as count")
            count = result.single()["count"]
            print(f"Nodes remaining in database: {count}")
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    response = input("This will delete ALL data in the database. Are you sure? (yes/no): ")
    if response.lower() == 'yes':
        clear_database()
    else:
        print("Operation cancelled.")
