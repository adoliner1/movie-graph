import sys
import os
from neo4j import GraphDatabase

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def check_constraints():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Show all constraints
            print("Current constraints:")
            result = session.run("SHOW CONSTRAINTS")
            for record in result:
                print(record)
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    check_constraints()