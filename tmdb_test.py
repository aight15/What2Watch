import os
from dotenv import load_dotenv
import tmdbsimple as tmdb

load_dotenv()
tmdb.API_KEY = os.getenv("TMDB_API_KEY")

search = tmdb.Search()
response = search.movie(query="Frozen")

for movie in search.results:
    print (movie ["title"])