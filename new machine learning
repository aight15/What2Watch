import os
import json
import requests
from dotenv import load_dotenv
from collections import Counter
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


#map moods to TMDB genre IDs
mood_to_genres = {
    "happy": [35, 10751],       # Comedy, Family    
    "sad": [18, 10749],         # Drama, Romance
    "adventurous": [12, 28],    # Adventure, Action
    "romantic": [10749, 35],    # Romance, Comedy
    "scared": [27, 53]          # Horror, Thriller
}

from collections import Counter

def get_favourite_genres(mood: str):
    #Look into liked_movies.json and find most common genres for this mood
    try:
        with open("liked_movies.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    mood_movies = [
        m for m in data if m["mood"] == mood and m.get("genres")
    ]

    if not mood_movies:
        return []
    
    counts = Counter()
    for m in mood_movies:
        for g in m.get("genres", []):
            counts[g] += 1
    return [g for g, _ in counts.most_common(3)]

def load_ratings_df():
    try:
        with open("liked_movies,json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return pd.DataFrame(columns=["user_id", "rating", "mood", "genres", "title"])
    
    #keep only dictionaries
    clean_rows = []
    for entry in data:
        if isinstance(entry, dict) and "id" in entry:
            clean_rows.append({
                "user_id": entry.get("user_id", "anonymous"),
                "movie_id": entry["id"],
                "title": entry.get("title", ""),
                "mood": entry.get("mood", ""),
                "genres": entry.get("genres", []),
                "rating": entry.get("rating", 5) 
            })

    if not clean_rows:
        return pd.DataFrame(columns=["user_id", "movie_id", "rating", "mood", "genres", "title"])
    return pd.DataFrame(clean_rows)
def build_user_item_matrix(ratings_df: pd.DataFrame):
    if ratings_df.empty:
        return pd.DataFrame()
    return ratings_df.pivot_table(
        index="user_id",
        columns="movie_id",
        values="rating",
        aggfunc="mean"
    )


def predict_scores_for_user(user_id: str, candidate_ids, ratings_df: pd.DataFrame):
    ui = build_user_item_matrix(ratings_df)
    if ui.empty:
        return {}

    # make sure current user is present
    if user_id not in ui.index:
        ui.loc[user_id] = np.nan

    ui_filled = ui.fillna(0)

    sims = cosine_similarity(ui_filled)
    sims_df = pd.DataFrame(sims, index=ui.index, columns=ui.index)

    # similarities from this user to others
    sim_series = sims_df.loc[user_id].drop(user_id, errors="ignore")
    sim_series = sim_series[sim_series > 0]  # only positive similarity

    if sim_series.empty:
        return {}

    scores = {}
    for mid in candidate_ids:
        if mid not in ui.columns:
            continue

        neighbor_ratings = ui[mid].dropna()
        if neighbor_ratings.empty:
            continue

        common_neighbors = sim_series[neighbor_ratings.index.intersection(sim_series.index)]
        if common_neighbors.empty:
            continue

        num = (neighbor_ratings[common_neighbors.index] * common_neighbors).sum()
        denom = np.abs(common_neighbors).sum()
        if denom > 0:
            scores[mid] = num / denom

    return scores


def get_seen_movie_ids(mood: str):
    #Return a set of movie IDs the user has already seen for this mood
    try:
        with open("liked_movies.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return set()
    seen = set()
    for entry in data:
       #make sure entry is a dictionary and not string
       if isinstance(entry, dict) and entry.get("mood") == mood and "id" in entry:
            seen.add(entry["id"])
    print (f"Seen IDs for mood", mood, ":", seen)
    return seen
#Load the key from .env file
load_dotenv()
api_key = os.getenv("TMDB_API_KEY")
print("DEBUG KEY:", api_key)


user_id = input("Who are you) (enter your name): ").strip()
if not user_id:
    user_id = "anonymous"

#ask the user for their mood
mood= input("How are you feeling today? (happy, sad, adventurous, romantic, scared): ")
mood = mood.strip().lower()

favourite_genres = get_favourite_genres(mood)
if favourite_genres:
    genre_ids = favourite_genres
else:
    genre_ids = mood_to_genres.get(mood.lower())

if genre_ids is None:
    #if user typed something weird, fall back to a general search
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={mood}"
else:
    genre_string = ",".join(str(g) for g in genre_ids)
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_string}&sort_by=popularity.desc"
response = requests.get(url)
data = response.json()

all_results = data.get("results", [])

seen_ids = get_seen_movie_ids(mood)
candidates = [m for m in all_results if m.get("id") not in seen_ids]

# load historical ratings
ratings_df = load_ratings_df()

if candidates:
    # IDs of candidate movies
    candidate_ids = [m["id"] for m in candidates if "id" in m]

    # predict scores based on similar users
    cf_scores = predict_scores_for_user(user_id, candidate_ids, ratings_df)

    if cf_scores:
        # sort candidates by predicted score (highest first)
        candidates.sort(
            key=lambda m: cf_scores.get(m.get("id"), 0),
            reverse=True
        )

    # take top 5 candidates (already sorted by CF or fallback original order)
    results = candidates[:5]
else:
    # if everything was seen, just fall back to top 5 from all_results
    results = all_results[:5]



# show top 5 movie results
print(f"\nTop 5 movie recommendations for your mood '{mood}':\n")

if not results:
    print("No movie recommendations found.")
    exit()

liked_movies = []

for idx, movie in enumerate(results, start=1):
    print(f"{idx}. {movie['title']}")

    # ask for rating 1–5
    while True:
        rating_str = input(
            f"Rate '{movie['title']}' from 1 to 5 (or press Enter to skip): "
        ).strip()

        if rating_str == "":
            rating = None
            break
        if rating_str.isdigit() and 1 <= int(rating_str) <= 5:
            rating = int(rating_str)
            break
        else:
            print("Please enter a number from 1 to 5, or just press Enter to skip.")

    if rating is not None:
        liked_movies.append({
            "user_id": user_id,
            "mood": mood,
            "id": movie["id"],
            "title": movie["title"],
            "genres": movie.get("genre_ids", []),
            "rating": rating,
        })

    print()


#save liked movies
if liked_movies:
    try:
        with open("liked_movies.json", "r") as f:
            existing = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []

    existing.extend(liked_movies)

    with open("liked_movies.json", "w") as f:
        json.dump(existing, f, indent=2)

    print("\nYour liked movies have been saved!")
else:
    print("\nNo liked movies have been saved!")

