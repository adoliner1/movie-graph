import sys
import os
from neo4j import GraphDatabase

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def fix_constraints():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Drop existing constraints
            print("Dropping existing constraints...")
            session.run("DROP CONSTRAINT movie_title IF EXISTS")
            session.run("DROP CONSTRAINT person_name IF EXISTS")
            
            # Create new constraints on ID
            print("Creating new constraints on ID...")
            session.run("CREATE CONSTRAINT movie_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.id IS UNIQUE")
            session.run("CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE")
            
            # Verify new constraints
            print("\nNew constraints:")
            result = session.run("SHOW CONSTRAINTS")
            for record in result:
                print(record)
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    print("This will update the database constraints to use ID instead of name/title")
    proceed = input("Continue? (yes/no): ")
    if proceed.lower() == 'yes':
        fix_constraints()
    else:
        print("Operation cancelled.")