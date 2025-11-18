import os
import json
import requests
from dotenv import load_dotenv

#Load the key from .env file
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

#ask the user for their mood
mood= input("How are you feeling today? (happy, sad, adventurous, romantic, scared): ")

#use mood as a search word on TMDB
url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={mood}"
response = requests.get(url)
data = response.json()

#show top 5 movie results
print(f"\nTop 5 movie recommendations for your mood '{mood}':\n")
for movie in data.get("results", []) [:5]:
    print("-", movie["title"])

liked_movies = []

for movie in data.get("results", [])[:5]:
    title = movie ["title"]
    print("-", title)
    liked = input(f"Did you like '{title}'? (yes/no): ")
    if liked.lower() == "yes":
        liked_movies.append(title)

#save liked movies
if liked_movies:
    with open("liked_movies.json", "a") as f:
        json.dump(liked_movies, f)
        f.write("\n")
    print("\n Your liked movies have been saved!")
else: 
    print("\nNo liked movies saved this time.")
                
