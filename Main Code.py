import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests
import random
import json
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

# ------------------- PAGE SETUP -------------------
st.set_page_config(page_title="What2Watch", page_icon="logo.jpg")

# ------------------- LOGO AND TITLE -------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=700)

if "page" not in st.session_state:
    st.session_state.page = "step1"

# ------------------- PAGE NAVIGATION -------------------
def goto(page_name):
    st.session_state.page = page_name

# ------------------- SIDE BAR ---------------------
st.sidebar.markdown("Let's see what genre you prefer: please click on the movies/series you would most rather watch right now?")

movies = [
    "Pixels",
    "The Conjuring",
    "Blade Runner 2049",
    "The Shawshank Redemption",
    "John Wick",
    "The Notebook"
]

series = [
    "Breaking Bad",
    "Stranger Things",
    "Friends",
    "The Office",
    "Game of Thrones",
    "Black Mirror"
]

genres = ["Comedy", "Horror", "Sci-Fi", "Drama", "Action", "Romance"]

title_genres = {
    "Pixels":               {"Comedy": 1, "Horror": 0, "Sci-Fi": 1, "Drama": 0, "Action": 1, "Romance": 0},
    "The Conjuring":        {"Comedy": 0, "Horror": 1, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},
    "Blade Runner 2049":    {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 1, "Romance": 0},
    "The Shawshank Redemption": {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 0},
    "John Wick":            {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 1, "Romance": 0},
    "The Notebook":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 1},

    "Breaking Bad":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 0},
    "Stranger Things":      {"Comedy": 0, "Horror": 1, "Sci-Fi": 1, "Drama": 1, "Action": 1, "Romance": 0},
    "Friends":              {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 1},
    "The Office":           {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},
    "Game of Thrones":      {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 1},
    "Black Mirror":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 0, "Romance": 0},
}

# Convert to list of chosen titles
selected_titles = []

st.sidebar.markdown("#### Movies")
for m in movies:
    if st.sidebar.checkbox(m, key=f"movie_{m}"):
        selected_titles.append(m)

st.sidebar.markdown("#### Series")
for s in series:
    if st.sidebar.checkbox(s, key=f"series_{s}"):
        selected_titles.append(s)

# --- CALCULATE GENRE SCORES ---
genre_scores = {g: 0 for g in genres}

for title in selected_titles:
    for g in genres:
        genre_scores[g] += title_genres[title][g]

values = [genre_scores[g] for g in genres]
values += values[:1]

# --- RADAR CHART ---
num_vars = len(genres)

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.25)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(genres)
ax.set_rlabel_position(30)

st.sidebar.pyplot(fig)

# ------------------- TMDB SETUP -------------------
TMDB_API_KEY = "ef26791dfc9c3b8254044fe9167e3edb"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

GENRE_MAP = {
    "Action": 28, "Comedy": 35, "Drama": 18, "Romance": 10749,
    "Horror": 27, "Sci-Fi": 878, "Documentary": 99,
    "Animation": 16, "Mystery": 9648, "Thriller": 53
}

# Fetches movies from TMDB by genre with optional filters for popularity, animation, runtime and release year
def get_movies_by_genre(genre_id, popularity_type="popular", animation_filter=None, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",
        "language": "en-US",
        "vote_count.gte": 100 if popularity_type == "popular" else 50
    }

    if animation_filter == "Animated":
        params["with_genres"] = f"{genre_id},16"
    elif animation_filter == "Live-action":
        params["without_genres"] = "16"

    if runtime_min:
        params["with_runtime.gte"] = runtime_min
    if runtime_max:
        params["with_runtime.lte"] = runtime_max
    
    if year_min:
        params["primary_release_date.gte"] = f"{year_min}-01-01"
    if year_max:
        params["primary_release_date.lte"] = f"{year_max}-12-31"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:num_results]
    return []

# Fetches TV series from TMDB by genre with optional filters for popularity, animation and air date
# NOTE: Runtime filters removed as they don't work reliably with TMDB's TV API
def get_series_by_genre(genre_id, popularity_type="popular", animation_filter=None, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    url = f"{TMDB_BASE_URL}/discover/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",
        "language": "en-US",
        "vote_count.gte": 50
    }

    if animation_filter == "Animated":
        params["with_genres"] = f"{genre_id},16"
    elif animation_filter == "Live-action":
        params["without_genres"] = "16"
    
    if year_min:
        params["first_air_date.gte"] = f"{year_min}-01-01"
    if year_max:
        params["first_air_date.lte"] = f"{year_max}-12-31"

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:num_results]
    return []

# Fetches movies from TMDB featuring or directed by a person, with optional filters for runtime and release year
def get_movies_by_actor_or_director(name, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    search_url = f"{TMDB_BASE_URL}/search/person"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": name,
        "language": "en-US"
    }
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200 and response.json()["results"]:
        person_id = response.json()["results"][0]["id"]
        discover_url = f"{TMDB_BASE_URL}/discover/movie"
        discover_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": person_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "language": "en-US"
        }
        
        if runtime_min:
            discover_params["with_runtime.gte"] = runtime_min
        if runtime_max:
            discover_params["with_runtime.lte"] = runtime_max
        if year_min:
            discover_params["primary_release_date.gte"] = f"{year_min}-01-01"
        if year_max:
            discover_params["primary_release_date.lte"] = f"{year_max}-12-31"
        
        movie_response = requests.get(discover_url, params=discover_params)
        if movie_response.status_code == 200:
            return movie_response.json().get("results", [])[:num_results]
    return []

# Fetches TV series from TMDB featuring a given actor, with optional filters for first air date
def get_series_by_actor(name, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    search_url = f"{TMDB_BASE_URL}/search/person"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": name,
        "language": "en-US"
    }
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200 and response.json()["results"]:
        person_id = response.json()["results"][0]["id"]
        discover_url = f"{TMDB_BASE_URL}/discover/tv"
        discover_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": person_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 30,
            "language": "en-US"
        }
        
        if year_min:
            discover_params["first_air_date.gte"] = f"{year_min}-01-01"
        if year_max:
            discover_params["first_air_date.lte"] = f"{year_max}-12-31"
        
        series_response = requests.get(discover_url, params=discover_params)
        if series_response.status_code == 200:
            return series_response.json().get("results", [])[:num_results]
    return []

# Fetches the top 10 highest-rated Ryan Gosling movies from TMDB, sorted by average vote
def get_ryan_gosling_movies():
    search_url = f"{TMDB_BASE_URL}/search/person"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": "Ryan Gosling",
        "language": "en-US"
    }
    person_response = requests.get(search_url, params=search_params)
    if person_response.status_code == 200 and person_response.json()['results']:
        gosling_id = person_response.json()['results'][0]['id']
        movie_url = f"{TMDB_BASE_URL}/discover/movie"
        movie_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": gosling_id,
            "sort_by": "vote_count.desc",
            "vote_count.gte": 50,
            "language": "en-US"
        }
        movie_response = requests.get(movie_url, params=movie_params)
        if movie_response.status_code == 200:
            movies = movie_response.json().get("results", [])
            sorted_movies = sorted(movies, key=lambda x: x.get("vote_average", 0), reverse=True)
            return sorted_movies[:10]
    return []

# Fetches a random popular movie from TMDB by selecting a random results page and movie
def get_random_movie():
    """Get a truly random popular movie"""
    random_page = random.randint(1, 50)
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": random_page
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            return random.choice(results)
    return None

# Fetches the YouTube trailer URL for a given movie or TV show from TMDB
def get_trailer(content_id, content_type="movie"):
    url = f"{TMDB_BASE_URL}/{content_type}/{content_id}/videos"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json().get("results", [])
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    return None


# ------------------- MACHINE LEARNING COMPONENT -------------------
def load_liked_movies():
    """Load user's liked movies from JSON file"""
    try:
        if Path("liked_movies.json").exists():
            with open("liked_movies.json", "r") as f:
                data = json.load(f)
                # Filter out invalid entries (strings, etc.)
                return [m for m in data if isinstance(m, dict) and "id" in m and m.get("liked") == True]
        return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_liked_movie(movie_id, title, genres, rating, liked=True):
    """Save a liked/disliked movie to the JSON file"""
    try:
        if Path("liked_movies.json").exists():
            with open("liked_movies.json", "r") as f:
                data = json.load(f)
                # Filter out invalid entries
                data = [m for m in data if isinstance(m, dict) and "id" in m]
        else:
            data = []
        
        # Remove existing entry for this movie if present
        data = [m for m in data if m.get("id") != movie_id]
        
        # Add new entry
        data.append({
            "id": movie_id,
            "title": title,
            "genres": genres,
            "rating": rating,
            "liked": liked
        })
        
        with open("liked_movies.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving preference: {e}")

def create_movie_feature_vector(movie):
    """Create a feature vector for a movie based on genres, rating, and popularity"""
    # Get all possible genre IDs from GENRE_MAP
    all_genre_ids = list(GENRE_MAP.values())
    
    # Create genre vector (binary: 1 if movie has genre, 0 otherwise)
    movie_genres = movie.get("genre_ids", [])
    genre_vector = [1 if genre_id in movie_genres else 0 for genre_id in all_genre_ids]
    
    # Normalize rating (0-10 scale, normalize to 0-1)
    rating = movie.get("vote_average", 5.0) / 10.0
    
    # Normalize popularity (using a simple log transform to reduce scale)
    popularity = movie.get("popularity", 0)
    popularity_normalized = np.log1p(popularity) / 20.0  # Rough normalization
    
    # Combine all features
    feature_vector = genre_vector + [rating, popularity_normalized]
    return np.array(feature_vector)

def reorder_movies_by_preference(movies, liked_movies_list):
    """Re-order movies based on similarity to user's liked movies using cosine similarity"""
    if not liked_movies_list or not movies:
        return movies
    
    # Create feature vectors for liked movies
    liked_vectors = []
    for liked_movie in liked_movies_list:
        # Reconstruct movie dict from saved data
        movie_dict = {
            "genre_ids": liked_movie.get("genres", []),
            "vote_average": liked_movie.get("rating", 5.0),
            "popularity": 50.0  # Default popularity if not stored
        }
        liked_vectors.append(create_movie_feature_vector(movie_dict))
    
    if not liked_vectors:
        return movies
    
    # Average the liked movie vectors to create a user preference profile
    user_profile = np.mean(liked_vectors, axis=0)
    
    # Calculate similarity scores for candidate movies
    movie_scores = []
    for movie in movies:
        movie_vector = create_movie_feature_vector(movie)
        # Calculate cosine similarity
        similarity = cosine_similarity([user_profile], [movie_vector])[0][0]
        movie_scores.append((movie, similarity))
    
    # Sort by similarity (highest first)
    movie_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return reordered movies
    return [movie for movie, score in movie_scores]

# Initializes an empty preferences dictionary in Streamlit session state if it doesn't exist
if "preferences" not in st.session_state:
    st.session_state.preferences = {}

# Displays centered/symetrical buttons in Streamlit to navigate to Random Movie or Ryan Gosling pages
def special_buttons():
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        if st.button("Random Movie", key="random_btn", use_container_width=True):
            goto("random")
    with col3:
        if st.button("Ryan Gosling", key="gosling_btn", use_container_width=True):
            goto("gosling")

# ------------------- STEP 1 -------------------
# Step 1 of the form: asks user for content type and stores it before moving to step 2
if st.session_state.page == "step1":
    special_buttons()
    st.title("What2Watch")
    with st.form("step1_form"):
        content_type = st.radio("Do you want to watch a movie, series, or both?", ["Film", "Series", "Both"])
        next_button = st.form_submit_button("Next")
    if next_button:
        st.session_state.preferences["content_type"] = content_type
        goto("step2")

# ------------------- STEP 2 -------------------
# Step 2 of the form: collects user's preferred content length and streaming services, with navigation controls
elif st.session_state.page == "step2":
    special_buttons()
    with st.form("step2_form"):
        content_type = st.session_state.preferences.get("content_type", "Film")
        if content_type == "Film":
            length = st.radio("Preferred movie length:", ["Short (< 90 min)", "Medium (90–120 min)", "Long (> 120 min)", "Any length"])
        elif content_type == "Series":
            length = st.radio("Preferred episode length:", ["< 30 min", "30–60 min", "60+ min", "Any length"])
        else:
            length = st.radio("Preferred duration:", [
                "Short Movie (< 90 min)",
                "Medium Movie (90–120 min)",
                "Long Movie (> 120 min)",
                "Short Episode (< 30 min)",
                "Standard Episode (30–60 min)",
                "Long Episode (> 60 min)",
                "Any length"
            ])

        streaming_services_options = ["Netflix", "Amazon Prime", "Disney+", "HBO Max", "Hulu", "Apple TV+", "Other"]
        streaming_services = []
        st.markdown("**Which streaming services do you have?**")
        for service in streaming_services_options:
            if st.checkbox(service):
                streaming_services.append(service)

        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("Back")
        with col2:
            next_button = st.form_submit_button("Next")

    if next_button:
        st.session_state.preferences["length"] = length
        st.session_state.preferences["streaming_services"] = streaming_services
        goto("step3")
    elif back_button:
        goto("step1")

# ------------------- STEP 3 -------------------
# Step 3 of the form: gathers detailed user preferences like genre, tone and favorite people before showing results
elif st.session_state.page == "step3":
    special_buttons()
    with st.form("step3_form"):
        content_type = st.session_state.preferences.get("content_type", "Film")
        
        # Show animation preference for all content types
        animation_preference = st.radio("Would you prefer animated or live-action?", ["Animated", "Live-action", "Both"])
        
        modern_or_classic = st.radio("Modern or classic?", ["Modern (2010+)", "Classic (before 2010)", "Doesn't matter"])
        watching_group = st.radio("Are you watching alone or in a group?", ["Alone", "In a group"])
        genre_choice = st.multiselect("Which genre are you interested in?", options=list(GENRE_MAP.keys()))
        popularity_type = st.radio("Do you want a well-known hit or a hidden gem?", ["Popular & trending", "Underrated", "Both"])

        # Always show the actor/director field
        actor_or_director = st.text_input("Any actors or directors you love? (optional)")

        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("Back")
        with col2:
            next_button = st.form_submit_button("Next")

    if next_button:
        st.session_state.preferences.update({
            "animation_preference": animation_preference,
            "modern_or_classic": modern_or_classic,
            "watching_group": watching_group,
            "genres": genre_choice,
            "popularity_type": popularity_type,
            "favorite_person": actor_or_director
        })
        goto("results")
    elif back_button:
        goto("step2")

# ------------------- RESULTS -------------------
elif st.session_state.page == "results":
    prefs = st.session_state.preferences
    content_type = prefs.get("content_type", "Film")
    
    if not prefs.get("genres"):
        st.warning("Please go back and select at least one genre.")
    else:
        # Parse length preferences for runtime filtering
        runtime_min, runtime_max = None, None
        episode_runtime_min, episode_runtime_max = None, None
        
        length = prefs.get("length", "")
        
        if "Short (< 90 min)" in length or "Short Movie" in length:
            runtime_max = 90
        elif "Medium (90–120 min)" in length or "Medium Movie" in length:
            runtime_min, runtime_max = 90, 120
        elif "Long (> 120 min)" in length or "Long Movie" in length:
            runtime_min = 120
        elif "< 30 min" in length or "Short Episode" in length:
            episode_runtime_max = 30
        elif "30–60 min" in length or "Standard Episode" in length:
            episode_runtime_min, episode_runtime_max = 30, 60
        elif "60+ min" in length or "Long Episode" in length:
            episode_runtime_min = 60
        
        # Parse year preferences
        year_min, year_max = None, None
        modern_or_classic = prefs.get("modern_or_classic", "Doesn't matter")
        if modern_or_classic == "Modern (2010+)":
            year_min = 2010
        elif modern_or_classic == "Classic (before 2010)":
            year_max = 2009
        
        # Determine popularity
        pop_type = "popular" if prefs["popularity_type"] == "Popular & trending" else "underrated"

        # Load liked movies for personalization
        liked_movies_list = load_liked_movies()
        
        # Show Movies
        if content_type in ["Film", "Both"]:
            st.subheader("Recommended Movies:")

            if liked_movies_list:
                st.info(f"Personalizing recommendations based on {len(liked_movies_list)}liked movie(s)!")
            
            for genre in prefs["genres"]:
                genre_id = GENRE_MAP.get(genre)
                if genre_id:
                    movies = get_movies_by_genre(
                        genre_id,
                        popularity_type=pop_type,
                        animation_filter=prefs.get("animation_preference"),
                        runtime_min=runtime_min,
                        runtime_max=runtime_max,
                        year_min=year_min,
                        year_max=year_max,
                        num_results=10
                    )

                    if not movies:
                        continue

                    #Re-rank movies using Machine Learning if user has liked movies
                    if liked_movies_list:
                        movies = reorder_movies_by_preference(movies, liked_movies_list)
                    
                    st.markdown(f"### {genre}")
                    for movie in movies:
                        title = movie.get("title")
                        overview = movie.get("overview", "No description available.")
                        poster_path = movie.get("poster_path")
                        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                        imdb_score = movie.get("vote_average")
                        movie_id = movie.get("id")
                        release_year = movie.get("release_date", "")[:4]
                        trailer_url = get_trailer(movie_id, "movie")
                        movie_genres = movie.get ("genre_ids",[])

                        #User can say if he/she likes/dislikes the movie
                        col1,col2 = st.columns([3,1])
                        with col1:
                            st.markdown(f"**{title}** ({release_year})")
                        with col2:
                            like_key = f"like_{movie_id}_{genre}"
                            dislike_key = f"dislike_{movie_id}_{genre}"

                            col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()
                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                        
                        if poster_url:
                            st.image(poster_url, width=150)
                        st.markdown(f"IMDb Score: {imdb_score}")
                        st.caption(overview)
                        if trailer_url:
                            st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                            st.markdown("---")
        
        # Show Series
        if content_type in ["Series", "Both"]:
            st.subheader("Recommended Series:")
            for genre in prefs["genres"]:
                genre_id = GENRE_MAP.get(genre)
                if genre_id:
                    series_list = get_series_by_genre(
                        genre_id,
                        popularity_type=pop_type,
                        animation_filter=prefs.get("animation_preference"),
                        episode_runtime_min=episode_runtime_min,
                        episode_runtime_max=episode_runtime_max,
                        year_min=year_min,
                        year_max=year_max,
                        num_results=10
                    )

            #Re-rank using Machine Learning
            if liked_movies_list and series_list:
                series_list = reorder_movies_by_preference(series_list, liked_movies_list)

            if series_list:
                st.markdown(f"### {genre}")
                for series in series_list:
                    title = series.get("name")
                    overview = series.get("overview", "No description available.")
                    poster_path = series.get("poster_path")
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                    imdb_score = series.get("vote_average")
                    series_id = series.get("id")
                    first_air_year = series.get("first_air_date", "")[:4]
                    trailer_url = get_trailer(series_id, "tv")
                    series_genres = series.get("genre_ids", [])
                    
                    # Header row + Like/Dislike
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{title}** ({first_air_year})")
                    with col2:
                        like_key = f"like_series_{series_id}_{genre}"
                        dislike_key = f"dislike_series_{series_id}_{genre}"

                        col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()

                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                  
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")                    

        # Show content by favorite actor/director
        if prefs.get("favorite_person"):
            if content_type in ["Film", "Both"]:
                st.subheader(f"Movies featuring **{prefs['favorite_person']}**:")
                person_movies = get_movies_by_actor_or_director(
                    prefs["favorite_person"],
                    runtime_min=runtime_min,
                    runtime_max=runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )

                #Re-rank using Machine Learning if user has liked the movie
                if liked_movies_list and person_movies:
                    person_movies = reorder_movies_by_preferences(person_movies, liked_movies_list)
                    
                for movie in person_movies:
                    title = movie.get("title")
                    overview = movie.get("overview", "No description available.")
                    poster_path = movie.get("poster_path")
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                    imdb_score = movie.get("vote_average")
                    movie_id = movie.get("id")
                    release_year = movie.get("release_date", "")[:4]
                    trailer_url = get_trailer(movie_id, "movie")
                    movie_genres = movie.get("genre_ids", [])

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{title}** ({release_year})")
                    with col2:
                        like_key = f"like_person_{movie_id}"
                        dislike_key = f"dislike_person_{movie_id}"
                
                        col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()
                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                 
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")
            
            if content_type in ["Series", "Both"]:
                st.subheader(f"Series featuring **{prefs['favorite_person']}**:")
                person_series = get_series_by_actor(
                    prefs["favorite_person"],
                    episode_runtime_min=episode_runtime_min,
                    episode_runtime_max=episode_runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )

                #Re-ranking using Machine Learning based on likes (movies+series)
                if liked_movies_list and person_series:
                    person_series = reorder_movies_by_preferences(person_series, liked_movies_list)
                
                for series in person_series:
                    title = series.get("name")
                    overview = series.get("overview", "No description available.")
                    poster_path = series.get("poster_path")
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                    imdb_score = series.get("vote_average")
                    series_id = series.get("id")
                    first_air_year = series.get("first_air_date", "")[:4]
                    trailer_url = get_trailer(series_id, "tv")
                    series_genres = series.get ("genre_ids", [])

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{title}** ({release_year})")
                    with col2:
                        like_key = f"like_person_{movie_id}"
                        dislike_key = f"dislike_person_{movie_id}"
                
                        col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()
                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                    
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")
        
        st.write("")  
        if st.button("Start Over"):
            goto("step1")

# ------------------- RANDOM MOVIE MODE -------------------
# Displays a random movie with its details and trailer, with options to refresh or return to the start
elif st.session_state.page == "random":
    st.title("Random Movie Generator")
    
    if st.button("Give me another random movie!"):
        st.rerun()
    
    random_movie = get_random_movie()
    if random_movie:
        title = random_movie.get("title")
        rating = random_movie.get("vote_average")
        overview = random_movie.get("overview", "No description available.")
        poster_path = random_movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        movie_id = random_movie.get("id")
        release_year = random_movie.get("release_date", "")[:4]
        trailer_url = get_trailer(movie_id, "movie")

        st.markdown(f"## {title} ({release_year})")
        if poster_url:
            st.image(poster_url, width=300)
        st.markdown(f"### IMDb Score: {rating}")
        st.markdown(f"Overview: {overview}")
        if trailer_url:
            st.markdown(f"### [Watch Trailer]({trailer_url})", unsafe_allow_html=True)
    else:
        st.warning("Could not fetch a random movie. Try again!")

    st.write("")  
    if st.button("← Back to Start"):
        goto("step1")

# ------------------- RYAN GOSLING MODE -------------------
# Displays a list of Ryan Gosling's highest-rated movies with posters, overviews and trailers
elif st.session_state.page == "gosling":
    st.title("Ryan Gosling Recommendations")
    gosling_movies = get_ryan_gosling_movies()
    if gosling_movies:
        st.markdown("Sorted by IMDb Score (Highest First)")
        for movie in gosling_movies:
            title = movie.get("title")
            rating = movie.get("vote_average")
            overview = movie.get("overview", "No description available.")
            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
            movie_id = movie.get("id")
            release_year = movie.get("release_date", "")[:4]
            trailer_url = get_trailer(movie_id, "movie")

            st.markdown(f"**{title}** ({release_year})")
            if poster_url:
                st.image(poster_url, width=150)
            st.markdown(f"IMDb Score: {rating}")
            st.caption(overview)
            if trailer_url:
                st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
            st.markdown("---")
    else:
        st.warning("No Ryan Gosling movies found.")

    st.write("")  
    if st.button("← Back to Start"):
        goto("step1")
