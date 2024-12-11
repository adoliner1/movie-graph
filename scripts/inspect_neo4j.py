import sys
import os
from neo4j import GraphDatabase
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def inspect_database():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Check what node labels exist
            print("\nNode types in database:")
            result = session.run("CALL db.labels()")
            labels = [record["label"] for record in result]
            print(labels)
            
            # Check what relationship types exist
            print("\nRelationship types in database:")
            result = session.run("CALL db.relationshipTypes()")
            rel_types = [record["relationshipType"] for record in result]
            print(rel_types)
            
            # Count of each type of node
            print("\nCounts of each node type:")
            for label in labels:
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
                count = result.single()["count"]
                print(f"{label}: {count} nodes")
                
            # Sample of nodes from each type
            print("\nSample nodes of each type:")
            for label in labels:
                print(f"\nSample {label} nodes:")
                result = session.run(f"MATCH (n:{label}) RETURN n LIMIT 3")
                for record in result:
                    pprint(dict(record["n"]))
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    print("Inspecting Neo4j database content...")
    inspect_database()