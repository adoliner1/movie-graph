import sys
import os
from neo4j import GraphDatabase
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def clean_schema():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Show current property keys
            print("Current property keys:")
            result = session.run("CALL db.propertyKeys()")
            current_keys = [record["propertyKey"] for record in result]
            print(current_keys)
            
            # Find properties actually in use
            print("\nProperties actually in use:")
            result = session.run("""
                MATCH (n)
                WITH DISTINCT keys(n) as keys
                UNWIND keys as key
                RETURN DISTINCT key
            """)
            used_keys = [record["key"] for record in result]
            print(used_keys)
            
            # Find unused keys
            unused_keys = set(current_keys) - set(used_keys)
            print("\nUnused property keys:")
            print(unused_keys)
            
            if unused_keys:
                print("\nDropping unused property keys...")
                # Unfortunately, Neo4j doesn't provide a direct way to drop property keys
                # The best we can do is note which ones are unused
                print("Note: Property keys cannot be directly dropped in Neo4j.")
                print("They will be automatically cleaned up when no longer referenced.")
                print("You may need to wait for the database to perform automatic cleanup.")
                
            print("\nCurrent node properties by label:")
            for label in ['Movie', 'Person']:
                result = session.run(f"""
                    MATCH (n:{label})
                    WITH DISTINCT keys(n) as keys
                    UNWIND keys as key
                    RETURN DISTINCT key
                """)
                keys = [record["key"] for record in result]
                print(f"\n{label} properties: {keys}")
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    clean_schema()