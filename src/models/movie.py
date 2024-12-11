class Movie:
    def __init__(self, tmdb_id, title, release_date, overview):
        self.tmdb_id = tmdb_id
        self.title = title
        self.release_date = release_date
        self.overview = overview

    @classmethod
    def from_tmdb_data(cls, data):
        """Create a Movie instance from TMDB API data"""
        return cls(
            tmdb_id=data['id'],
            title=data['title'],
            release_date=data['release_date'],
            overview=data['overview']
        )