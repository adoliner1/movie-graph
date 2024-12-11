from dataclasses import dataclass
from typing import List

@dataclass
class MovieNode:
    id: int
    title: str
    release_date: str
    overview: str
    tagline: str
    genres: List[str]

@dataclass
class PersonNode:
    id: int
    name: str
    profile_path: str
    popularity: float

@dataclass(frozen=True)  # frozen=True makes it hashable for use in sets
class Relationship:
    person_id: int
    movie_id: int
    type: str  # 'ACTED_IN' or 'DIRECTED'
    character: str = ''  # Only for ACTED_IN
    order: int = -1     # Only for ACTED_IN, -1 for DIRECTED