class Person:
    def __init__(self, tmdb_id, name, birthday=None, biography=None):
        self.tmdb_id = tmdb_id
        self.name = name
        self.birthday = birthday
        self.biography = biography

    @classmethod
    def from_tmdb_data(cls, data):
        """Create a Person instance from TMDB API data"""
        return cls(
            tmdb_id=data['id'],
            name=data['name'],
            birthday=data.get('birthday'),
            biography=data.get('biography')
        )