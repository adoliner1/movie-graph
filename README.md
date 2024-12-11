# Movie Graph Database

A tool to create a Neo4j graph database of movies using The Movie Database (TMDB) as a data source.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Create a .env file with your credentials:
```
TMDB_API_KEY=your_api_key_here
NEO4J_URI=neo4j+s://your-neo4j-instance:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password_here
```

## Usage

The tool provides several commands through `movie_graph.py`:

### Setup Database
Initialize or reset Neo4j constraints:
```bash
python movie_graph.py setup
```

### Clear Database
Remove all nodes and relationships:
```bash
python movie_graph.py clear
```

### Import Movies
Import movies sorted by rating:
```bash
# Import first 250 highest-rated movies
python movie_graph.py import --count 250 --start 1

# Import next 250 movies
python movie_graph.py import --count 250 --start 251

# Import with automatic confirmation
python movie_graph.py import --count 100 --yes
```

## Project Structure

- `src/`
  - `config.py` - Configuration and environment variables
  - `tmdb_client.py` - TMDB API client
  - `neo4j_client.py` - Neo4j database operations
  - `transformer.py` - Data transformation logic
  - `models/` - Data models for movies, people, and relationships
- `movie_graph.py` - Main CLI tool
- `requirements.txt` - Python dependencies

## Data Model

The graph database consists of:
- Movie nodes with properties: id, title, release_date, overview, tagline, genres
- Person nodes with properties: id, name, profile_path, popularity
- Relationships:
  - ACTED_IN (Person → Movie) with properties: character, order
  - DIRECTED (Person → Movie)