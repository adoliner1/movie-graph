import sys
import os
from neo4j import GraphDatabase
from pprint import pprint

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.config import Config

def check_properties():
    uri = "neo4j+s://c79bb620.databases.neo4j.io:7687"
    driver = None
    try:
        driver = GraphDatabase.driver(uri, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        with driver.session() as session:
            # Check all properties actually being used on Person nodes
            print("Properties actually in use on Person nodes:")
            result = session.run("""
                MATCH (p:Person)
                WITH DISTINCT keys(p) as keys
                UNWIND keys as key
                RETURN DISTINCT key
            """)
            person_properties = [record["key"] for record in result]
            print(person_properties)
            
            # Check if any nodes have the 'born' property
            print("\nNodes with 'born' property:")
            result = session.run("""
                MATCH (p:Person)
                WHERE EXISTS(p.born)
                RETURN p.name, p.born
            """)
            nodes_with_born = list(result)
            if nodes_with_born:
                for record in nodes_with_born:
                    print(f"{record['p.name']}: {record['p.born']}")
            else:
                print("No nodes found with 'born' property")
            
    except Exception as e:
        print(f"Query failed: {str(e)}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    check_properties()