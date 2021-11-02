import requests

MOVIE_API_KEY = "df0e286329d9de2ba7016c5388623d43"
# website https://www.themoviedb.org/settings/api
MOVIE_DB_SEARCH_UR = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

class MovieSelector():
    def search_movie(self, user_query):
        data = {
            "api_key": MOVIE_API_KEY,
            "query": user_query
        }
        results = requests.get(url=MOVIE_DB_SEARCH_UR, params=data).json()['results']
        return results

    def get_movie_data(self, movie_id):
        data = {
            "api_key": MOVIE_API_KEY,
            "language": "en-US"
        }
        results = requests.get(url=f"{MOVIE_DB_INFO_URL}/{movie_id}", params=data).json()
        return results

