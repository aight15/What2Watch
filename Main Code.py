# Importation of necessary libraries for the application
import streamlit as st  # Web framework for creating the UI
import matplotlib.pyplot as plt  # Plotting library for creating the radar chart
import numpy as np  # Numerical operations library for arrays and math
import requests  # HTTP library for making API calls to TMDB
import random  # Random number generation for random movie feature
import json  # JSON parsing library for saving/loading user preferences
from sklearn.metrics.pairwise import cosine_similarity  # ML library for calculating similarity scores
from pathlib import Path  # File path handling library

# PAGE SETUP
# Configuration of the Streamlit page with title and icon
st.set_page_config(page_title="What2Watch", page_icon="logo.jpg")

# LOGO AND TITLE
# Creation of three columns with specific width ratios for centering the logo
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image("logo.jpg", width=700)

# Initialization of the page navigation state if not already set
# Setting the default starting page to step1
if "page" not in st.session_state:
    st.session_state.page = "step1"

# PAGE NAVIGATION
# Function to change the current page in the application
def goto(page_name):
    """Navigate to a different page by updating session state"""
    st.session_state.page = page_name

# SIDE BAR
# Displaying sidebar instructions for the genre preference
st.sidebar.markdown("Uncertain which genre you like? Select below which movies and series you've enjoyed and figure out what your prefered genre is.")

# Definition of predefined lists of movies for genre analysis
movies = [
    "Pixels",  # Comedy/Sci-Fi/Action movie
    "The Conjuring",  # Horror movie
    "Blade Runner 2049",  # Sci-Fi/Drama/Action movie
    "The Shawshank Redemption",  # Drama movie
    "John Wick",  # Action movie
    "The Notebook"  # Drama/Romance movie
]

# Definition of predefined lists of TV series for genre analysis
series = [
    "Breaking Bad",  # Drama/Action series
    "Stranger Things",  # Horror/Sci-Fi/Action series
    "Friends",  # Comedy/Romance series
    "The Office",  # Comedy series
    "Game of Thrones",  # Drama/Action/Romance series
    "Black Mirror"  # Sci-Fi/Drama series
]

# Definition of the genre categories used in the radar chart
genres = ["Comedy", "Horror", "Sci-Fi", "Drama", "Action", "Romance"]  # List of all available genres

# Map of each title to its genre composition
title_genres = {
    "Pixels":               {"Comedy": 1, "Horror": 0, "Sci-Fi": 1, "Drama": 0, "Action": 1, "Romance": 0},
    "The Conjuring":        {"Comedy": 0, "Horror": 1, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},
    "Blade Runner 2049":    {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 1, "Romance": 0},
    "The Shawshank Redemption": {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 0},
    "John Wick":            {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 1, "Romance": 0},
    "The Notebook":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 0.4},

    "Breaking Bad":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 0},
    "Stranger Things":      {"Comedy": 0, "Horror": 1, "Sci-Fi": 1, "Drama": 0, "Action": 1, "Romance": 0},
    "Friends":              {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0.4},
    "The Office":           {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},
    "Game of Thrones":      {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 0},
    "Black Mirror":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 0, "Romance": 0},
}

# Creation of empty list to store user's selected titles based on checkbox selections
selected_titles = []

# Displaying movie checkboxes in the sidebar
# Looping through each movie in the list and adding movie to selected list if checked
st.sidebar.markdown("#### Movies")
for m in movies:  # Loop through each movie in the list
    if st.sidebar.checkbox(m, key=f"movie_{m}"):
        selected_titles.append(m)

# Displaying series checkboxes in the sidebar
# Looping through each series in the list and adding series to selected list if checked
st.sidebar.markdown("#### Series")
for s in series:  # Loop through each series in the list
    if st.sidebar.checkbox(s, key=f"series_{s}"):
        selected_titles.append(s)  # Add series to selected list if checked

# CALCULATE GENRE SCORES
# Initialization of all genre scores to zero
genre_scores = {g: 0 for g in genres}

# Calculatation of total score for each genre based on selected titles
# Looping through each title which the user selected and looping through each genre
# Adding genre value from title to total score
for title in selected_titles:
    for g in genres:
        genre_scores[g] += title_genres[title][g]

# Preparation of values for radar chart by extracting scores in order
values = [genre_scores[g] for g in genres]  # Convert dictionary to ordered list
values += values[:1]  # Duplicate first value at end to close the radar chart polygon

# RADAR CHART
# Calculation of number of genre axes for the chart
num_vars = len(genres)

# Calculatation of angle for each axis in radians
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# Creation of polar subplot for radar chart
fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

# Plotting the genre scores as a line on the radar chart
ax.plot(angles, values, linewidth=2)
# Filling the area inside the radar chart
ax.fill(angles, values, alpha=0.25)

# Setting the position and labels for each axis with genre name
ax.set_xticks(angles[:-1])
ax.set_xticklabels(genres)
ax.set_rlabel_position(30)

# Displaying the radar chart in the sidebar based on user selection
st.sidebar.pyplot(fig)

# TMDB SETUP
# Showing the TMDB API Key and URL
TMDB_API_KEY = "ef26791dfc9c3b8254044fe9167e3edb"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Mapping the genre names to TMDB genre IDs for movies
MOVIE_GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Romance": 10749,
    "Horror": 27,
    "Sci-Fi": 878,
    "Documentary": 99,
    "Animation": 16,
    "Mystery": 9648,
    "Thriller": 53
}

# Mapping the genre names to TMDB genre IDs for TV series
TV_GENRE_MAP = {
    "Action": 10759,
    "Comedy": 35,
    "Drama": 18,
    "Sci-Fi": 10765,
    "Documentary": 99,
    "Animation": 16,
    "Mystery": 9648,
    "Crime": 80
}

# TMDB API FUNCTIONS
# Function to fetch movies from TMDB based on genre and various filters
# Optional filters are popularity, animation, runtime, release year
# Usage of the MOVIE_GENRE_MAP
def get_movies_by_genre(genre_name, popularity_type="popular", animation_filter=None, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches movies from TMDB by genre with optional filters for popularity, animation, runtime and release year"""
    genre_id = MOVIE_GENRE_MAP.get(genre_name)
    if not genre_id:
        return []
    
    url = f"{TMDB_BASE_URL}/discover/movie"
    # Set up for query parameters for the API request
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",
        "language": "en-US",
        "vote_count.gte": 100 if popularity_type == "popular" else 50  # Minimum votes filter (higher for popular)
    }

    # Application of animation filter or live-action filter if specified
    if animation_filter == "Animated":
        params["with_genres"] = f"{genre_id},16"
    elif animation_filter == "Live-action":
        params["without_genres"] = "16"

    # Application of runtime filters if specified
    if runtime_min:
        params["with_runtime.gte"] = runtime_min
    if runtime_max:
        params["with_runtime.lte"] = runtime_max
    
    # Application of release date filters if specified
    if year_min:
        params["primary_release_date.gte"] = f"{year_min}-01-01"
    if year_max:
        params["primary_release_date.lte"] = f"{year_max}-12-31"

    # Making the API request with checking if the request was successful
    # Return of empty list if request failed
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:num_results]
    return []

# Function to fetch TV series from TMDB based on genre and various filters
# Optional filters are popularity, animation, air date
# Usage of the TV_GENRE_MAP
def get_series_by_genre(genre_name, popularity_type="popular", animation_filter=None, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches TV series from TMDB by genre with optional filters for popularity, animation and air date"""
    genre_id = TV_GENRE_MAP.get(genre_name)  # Use TV_GENRE_MAP
    if not genre_id:
        return []
    
    url = f"{TMDB_BASE_URL}/discover/tv"
    # Set up for query parameters for the API request
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",
        "language": "en-US",
        "vote_count.gte": 50
    }

    # Application of animation filter or live-action filter if specified
    if animation_filter == "Animated":  # User wants only animated content
        params["with_genres"] = f"{genre_id},16"  # Add animation genre ID (16) to filter
    elif animation_filter == "Live-action":  # User wants only live-action content
        params["without_genres"] = "16"  # Exclude animation genre
    
    # Application of air date filters if specified
    if year_min:
        params["first_air_date.gte"] = f"{year_min}-01-01"
    if year_max:
        params["first_air_date.lte"] = f"{year_max}-12-31"

    # Making the API request with checking if the request was successful
    # Return of empty list if request failed
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:num_results]
    return []

# Function to fetch movies featuring or directed by a specific person
def get_movies_by_actor_or_director(name, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches movies from TMDB featuring or directed by a person, with optional filters for runtime and release year"""
    # Search for the person by name
    search_url = f"{TMDB_BASE_URL}/search/person"
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": name,
        "language": "en-US"
    }
    # Sending request to search for person and check if search was successful
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200 and response.json()["results"]:
        person_id = response.json()["results"][0]["id"]
        # Search for movies featuring this person
        discover_url = f"{TMDB_BASE_URL}/discover/movie"
        discover_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": person_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 50,
            "language": "en-US"
        }
        
        # Applying runtime filters if specified
        if runtime_min:
            discover_params["with_runtime.gte"] = runtime_min
        if runtime_max:
            discover_params["with_runtime.lte"] = runtime_max
        # Applying year filters if specified
        if year_min:
            discover_params["primary_release_date.gte"] = f"{year_min}-01-01"
        if year_max:
            discover_params["primary_release_date.lte"] = f"{year_max}-12-31"
        
        # Making the TMBD API request for movies and returning first movies
        movie_response = requests.get(discover_url, params=discover_params)
        if movie_response.status_code == 200:
            return movie_response.json().get("results", [])[:num_results]
    return []  # Returning empty list if search or request failed

# Function to fetch TV series featuring a specific actor
def get_series_by_actor(name, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches TV series from TMDB featuring a given actor, with optional filters for first air date"""
    # First, searching for the person by name
    search_url = f"{TMDB_BASE_URL}/search/person"  # Building URL for person search endpoint
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": name,
        "language": "en-US"  # Requesting English language results
    }
    # Sending request to search for person and getting the ID of the first matching person
    response = requests.get(search_url, params=search_params)
    if response.status_code == 200 and response.json()["results"]:
        person_id = response.json()["results"][0]["id"]
        # Searching for TV series featuring this person and building URL for TV discovery
        discover_url = f"{TMDB_BASE_URL}/discover/tv"
        discover_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": person_id,
            "sort_by": "popularity.desc",
            "vote_count.gte": 30,
            "language": "en-US"
        }
        
        # Applying year filters if specified by user
        if year_min:
            discover_params["first_air_date.gte"] = f"{year_min}-01-01"
        if year_max:
            discover_params["first_air_date.lte"] = f"{year_max}-12-31"
        
        # Making the TMDB API request for series
        series_response = requests.get(discover_url, params=discover_params)
        if series_response.status_code == 200:
            return series_response.json().get("results", [])[:num_results]  # Returning first num_results series
    return []  # Returning empty list if search or request failed

# Function to fetch Ryan Gosling's top-rated movies
def get_ryan_gosling_movies():
    """Fetches the top 10 highest-rated Ryan Gosling movies from TMDB, sorted by average vote"""
    # First, searching for Ryan Gosling
    search_url = f"{TMDB_BASE_URL}/search/person"  # Building URL for person search
    search_params = {
        "api_key": TMDB_API_KEY,
        "query": "Ryan Gosling",
        "language": "en-US"
    }
    person_response = requests.get(search_url, params=search_params)  # Sending GET request to search for Ryan Gosling
    if person_response.status_code == 200 and person_response.json()['results']:
        gosling_id = person_response.json()['results'][0]['id']
        # Getting movies featuring Ryan Gosling
        movie_url = f"{TMDB_BASE_URL}/discover/movie"  # Building URL for movie discovery
        movie_params = {
            "api_key": TMDB_API_KEY,
            "with_cast": gosling_id,
            "sort_by": "vote_count.desc",
            "vote_count.gte": 50,
            "language": "en-US"
        }
        # Sending request to TMDB and getting list of 10 movies if successful
        movie_response = requests.get(movie_url, params=movie_params)
        if movie_response.status_code == 200:
            movies = movie_response.json().get("results", [])
            sorted_movies = sorted(movies, key=lambda x: x.get("vote_average", 0), reverse=True)
            return sorted_movies[:10]
    return []  # Returning empty list if search or request failed

# Function to get a random popular movie and building URL for popular movies
def get_random_movie():
    """Get a truly random popular movie by selecting a random results page and movie"""
    random_page = random.randint(1, 50)
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "page": random_page
    }
    # Sending request to TMDB and checking if request was successful for getting list of movies from that page
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json().get("results", [])
        # If the page has results it returns a random movie from the page
        if results:
            return random.choice(results)
    return None  # Returning nothing if request failed or no results

# Function to fetch trailer URL for a movie or TV show and building URL for videos
def get_trailer(content_id, content_type="movie"):
    """Fetches the YouTube trailer URL for a given movie or TV show from TMDB"""
    url = f"{TMDB_BASE_URL}/{content_type}/{content_id}/videos"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    # Sending request to TMDB and checking if request was successful for getting list of videos
    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json().get("results", [])
        # Looping through each video and checking if it's a YouTube trailer which will return the YouTube URL
        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    return None  # Returning nothing if no trailer found


# MACHINE LEARNING COMPONENT
# Function to load user's liked movies from JSON file
def load_liked_movies():
    """Load user's liked movies from JSON file"""
    try:
        # Check if file exists and opening of file
        if Path("liked_movies.json").exists():
            with open("liked_movies.json", "r") as f:
                data = json.load(f)
                # Filtering out invalid entries (strings, etc.) to return only valid liked movies
                return [m for m in data if isinstance(m, dict) and "id" in m and m.get("liked") == True]
        return []
        # Catching of error and return of empty list if error occurs
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if error occurs

# Function to save a liked or disliked movie to the JSON file
def save_liked_movie(movie_id, title, genres, rating, liked=True):
    """Save a liked/disliked movie to the JSON file"""
    try:
        # Check if file exists and opening of file for reading
        if Path("liked_movies.json").exists():
            with open("liked_movies.json", "r") as f:
                data = json.load(f)
                # Filtering out invalid entries and keeping only valid entries
                data = [m for m in data if isinstance(m, dict) and "id" in m]
        else:
            data = []
        
        # Removing existing entry for this movie if present
        data = [m for m in data if m.get("id") != movie_id]  # Filter out this movie ID
        
        # Adding the new entry
        data.append({
            "id": movie_id,  # Movie's TMDB ID
            "title": title,  # Movie title
            "genres": genres,  # List of genre IDs
            "rating": rating,  # IMDb score
            "liked": liked  # Whether user liked (True) or disliked (False)
        })
        
        # Saving of updated data to file
        with open("liked_movies.json", "w") as f:
            json.dump(data, f, indent=2)
    # Catching of errors and displaying error message if error occurs         
    except Exception as e:
        st.error(f"Error saving preference: {e}")

# Function to create a feature vector for machine learning
def create_movie_feature_vector(movie):
    """Create a feature vector for a movie based on genres, rating, and popularity"""
    # Getting all possible genre IDs
    # Genre IDs from both MOVIE_GENRE_MAP and TV_GENRE_MAP
    all_genre_ids = list(set(list(MOVIE_GENRE_MAP.values()) + list(TV_GENRE_MAP.values())))
    
    # Creation of genre vector
    movie_genres = movie.get("genre_ids", [])
    genre_vector = [1 if genre_id in movie_genres else 0 for genre_id in all_genre_ids]
    
    # Normalization of rating
    rating = movie.get("vote_average", 5.0) / 10.0
    
    # Normalization of popularity
    popularity = movie.get("popularity", 0)
    popularity_normalized = np.log1p(popularity) / 20.0
    
    # Combination of all features into single vector for ML operation
    feature_vector = genre_vector + [rating, popularity_normalized]
    return np.array(feature_vector)

# Function to reorder movies based on user preferences using ML
# Goal to improve user's movies/series suggestions
def reorder_movies_by_preference(movies, liked_movies_list):
    """Re-order movies based on similarity to user's liked movies using cosine similarity"""
    if not liked_movies_list or not movies:
        return movies
    
    # Creation of vectors for liked movies
    # Loop through each liked movie
    liked_vectors = []
    for liked_movie in liked_movies_list:
        # Reconstruct movie dictionary from saved data
        # Getting saved genre IDs and rating
        movie_dict = {
            "genre_ids": liked_movie.get("genres", []),  # Get saved genre IDs
            "vote_average": liked_movie.get("rating", 5.0),  # Get saved rating
            "popularity": 50.0  # Default popularity if not stored
        }
        # Creation and addition of feature vector
        liked_vectors.append(create_movie_feature_vector(movie_dict))

    # Check of created vector and return of original order if no vector was created
    if not liked_vectors:
        return movies
    
    # Creation of user preference profile by average of liked movie vector
    user_profile = np.mean(liked_vectors, axis=0)
    
    # Calculation of similarity scores to ensure comparability
    # Loop through each movie and creation of vector
    movie_scores = [] 
    for movie in movies:
        movie_vector = create_movie_feature_vector(movie)
        # Calculation of similarity between user profile and movie
        # Addition of movie and its score to list
        similarity = cosine_similarity([user_profile], [movie_vector])[0][0]
        movie_scores.append((movie, similarity))
    
    # Sorting of scores by similarity with highest score first
    movie_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return of reordered movies
    return [movie for movie, score in movie_scores]  # Extract just the movies in sorted order

# Initialization of preferences dictionary for storing user preferences
if "preferences" not in st.session_state:
    st.session_state.preferences = {}

# Display of buttons for special features (random, Ryan Gosling)
def special_buttons():
    """Displays centered/symmetrical buttons in Streamlit to navigate to Random Movie or Ryan Gosling pages"""
    col1, col2, col3 = st.columns([2, 3, 2])
    with col1:
        if st.button("Random Movie", key="random_btn", use_container_width=True):
            goto("random")
            st.rerun()
    with col3:
        if st.button("Ryan Gosling", key="gosling_btn", use_container_width=True):
            goto("gosling")
            st.rerun()

# STEP 1
# Step 1: Asking user for content type (Film, Serie)
# Display of Random Movie and Ryan Gosling buttons
if st.session_state.page == "step1":
    special_buttons()
    st.title("What2Watch")
    with st.form("step1_form"):
        content_type = st.radio("Do you want to watch a movie or a serie?", ["Film", "Series"])
        next_button = st.form_submit_button("Next")
    if next_button:
        st.session_state.preferences["content_type"] = content_type
        goto("step2")
        st.rerun()

# STEP 2
# Step 2: Collection of all user preferences
# Display of Random Movie and Ryan Gosling buttons
elif st.session_state.page == "step2":
    special_buttons()
    with st.form("step2_form"):
        content_type = st.session_state.preferences.get("content_type", "Film")
        
        # Preference of length based on content type
        if content_type == "Film":
            length = st.radio("Preferred movie length:", ["Short (< 90 min)", "Medium (90–120 min)", "Long (> 120 min)", "Any length"])
        elif content_type == "Series":
            length = st.radio("Preferred episode length:", ["< 30 min", "30–60 min", "60+ min", "Any length"])

        # Preference of animation or live-action
        animation_preference = st.radio("Would you prefer animated or live-action?", ["Animated", "Live-action", "Both"])
        
        # Preference of modern or classic
        modern_or_classic = st.radio("Modern or classic?", ["Modern (2010+)", "Classic (before 2010)", "Doesn't matter"])
        
        # Selection of genre with preferred genre hint from the sidebar
        # Determination of preferred genre from sidebar if any titles selected
        preferred_genre_text = ""
        if selected_titles:
            max_score = max(genre_scores.values())
            if max_score > 0:
                top_genres = [g for g, score in genre_scores.items() if score == max_score]
                if len(top_genres) == 1:
                    preferred_genre_text = f"(Your preferred genre is **{top_genres[0]}**)"
                else:  # Multiple top genres
                    preferred_genre_text = f"(Your preferred genres are **{', '.join(top_genres)}**)"

        # Selection of genres
        # Options depend on content type
        st.markdown(f"**Which genre are you interested in?** {preferred_genre_text}")
        if content_type == "Film":
             genre_choice = st.multiselect("", options=list(MOVIE_GENRE_MAP.keys()), label_visibility="collapsed")
        elif content_type == "Series":
            genre_choice = st.multiselect("", options=list(TV_GENRE_MAP.keys()), label_visibility="collapsed")
       

        # Preference of popularity
        popularity_type = st.radio("Do you want a well-known hit or a hidden gem?", ["Popular & trending", "Underrated", "Both"])  # Radio buttons for popularity

        # Optional addition of actor/director
        actor_or_director = st.text_input("Any actors or directors you love? (optional)")

        # Navigation of buttons
        col1, col2 = st.columns(2)
        with col1:
            back_button = st.form_submit_button("Back")
        with col2:
            next_button = st.form_submit_button("Next")

    # Saving of user preferences and update of preference state
    # Navigation to result page and generated recommendations
    if next_button:
        st.session_state.preferences.update({
            "length": length,
            "animation_preference": animation_preference,
            "modern_or_classic": modern_or_classic,
            "genres": genre_choice,
            "popularity_type": popularity_type,
            "favorite_person": actor_or_director
        })
        goto("results")
        st.rerun()
    elif back_button:
        goto("step1")
        st.rerun()

# RESULTS
# Results page: displays personalized movie and series recommendations
# Checking if current page is results and getting all preferences from session
elif st.session_state.page == "results":
    prefs = st.session_state.preferences
    content_type = prefs.get("content_type", "Film")
    
    # Validating that user selected at least one genre
    if not prefs.get("genres"):
        st.warning("Please go back and select at least one genre.")  # Showing warning message
    else:
        # If user selected genres, proceeing with recommendations
        runtime_min, runtime_max = None, None
        episode_runtime_min, episode_runtime_max = None, None
        # Getting length preference from before
        length = prefs.get("length", "")
        
        # Mapping length preferences to runtime filter values for movies
        if "Short (< 90 min)" in length or "Short Movie" in length:
            runtime_max = 90
        elif "Medium (90–120 min)" in length or "Medium Movie" in length:
            runtime_min, runtime_max = 90, 120
        elif "Long (> 120 min)" in length or "Long Movie" in length:
            runtime_min = 120
        # Mapping length preferences to runtime filter values for series
        elif "< 30 min" in length or "Short Episode" in length:
            episode_runtime_max = 30
        elif "30–60 min" in length or "Standard Episode" in length:
            episode_runtime_min, episode_runtime_max = 30, 60
        elif "60+ min" in length or "Long Episode" in length:
            episode_runtime_min = 60
        
        # Initializing year filter variables and getting era preference
        year_min, year_max = None, None  # 
        modern_or_classic = prefs.get("modern_or_classic", "Doesn't matter")
        if modern_or_classic == "Modern (2010+)":
            year_min = 2010
        elif modern_or_classic == "Classic (before 2010)":
            year_max = 2009
        
        # Determining popularity type for API calls
        pop_type = "popular" if prefs["popularity_type"] == "Popular & trending" else "underrated"  # Map UI choice to API parameter

        # Loading liked movies for personalization with Machine Learning and loading user's liked movies from JSON file
        liked_movies_list = load_liked_movies()
        
        # Showing Movies section
        if content_type in ["Film"]:
            st.subheader("Recommended Movies:")

            # Showing personalization info if user has liked movies
            if liked_movies_list:
                st.info(f"Personalizing recommendations based on {len(liked_movies_list)} liked movie(s)!")
            
            # Looping through each selected genre
            for genre in prefs["genres"]:
                # Getting movies from TMDB API (and now passing genre name instead of ID)
                movies = get_movies_by_genre(
                    genre,
                    popularity_type=pop_type,
                    animation_filter=prefs.get("animation_preference"),
                    runtime_min=runtime_min,
                    runtime_max=runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )
                # Checking if API returned any movies and skipping to next genre if no movies found
                if not movies:
                    continue

                # Re-ranking movies using Machine Learning if user has liked movies
                if liked_movies_list:
                    # Applying ML-based reordering
                    movies = reorder_movies_by_preference(movies, liked_movies_list)
                
                st.markdown(f"### {genre}")
                # Looping through each movie in the results to get needed data
                for movie in movies:
                    title = movie.get("title")
                    overview = movie.get("overview", "No description available.")
                    poster_path = movie.get("poster_path")
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                    imdb_score = movie.get("vote_average")
                    movie_id = movie.get("id")
                    release_year = movie.get("release_date", "")[:4]
                    trailer_url = get_trailer(movie_id, "movie")
                    movie_genres = movie.get("genre_ids",[])

                    # Creating header row with Like/Dislike buttons
                    col1,col2 = st.columns([3,1])
                    with col1:
                        st.markdown(f"**{title}** ({release_year})")
                    with col2:
                        like_key = f"like_{movie_id}_{genre}"
                        dislike_key = f"dislike_{movie_id}_{genre}"

                        col_like, col_dislike = st.columns(2)
                    with col_like:
                        if st.button("Like", key=like_key):
                            # Saving liked movies and refreshing page to apply changes
                            save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)
                            st.success(f"Saved '{title}' to your preferences!")
                            st.rerun()
                    with col_dislike:
                        if st.button("Dislike", key=dislike_key):
                            # Saving disliked movies and refreshing page to apply changes
                            save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)
                            st.info(f"Noted that you don't like '{title}'")
                            st.rerun()
                    
                    # Displaying movie details
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")
        
        # Showing Series section
        if content_type in ["Series"]:
            st.subheader("Recommended Series:")

            if liked_movies_list:
                st.info(f"Personalizing recommendations based on {len(liked_movies_list)} liked title(s)")

            # Looping through each selected genre
            for genre in prefs["genres"]:
                # Getting series from TMDB API (and now passing genre name instead of ID)
                series_list = get_series_by_genre(
                    genre,
                    popularity_type=pop_type,
                    animation_filter=prefs.get("animation_preference"),
                    episode_runtime_min=episode_runtime_min,
                    episode_runtime_max=episode_runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )

                # Re-ranking using Machine Learning if user has liked series
                if liked_movies_list and series_list:
                    # Applying ML-based reordering
                    series_list = reorder_movies_by_preference(series_list, liked_movies_list)

                if series_list:
                    st.markdown(f"### {genre}")
                    # Looping through each series in the results to get needed data
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
                        
                        # Creating header row with Like/Dislike buttons
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{title}** ({first_air_year})")
                        with col2:
                            like_key = f"like_series_{series_id}_{genre}"
                            dislike_key = f"dislike_series_{series_id}_{genre}"

                            col_like, col_dislike = st.columns(2)
                            with col_like:
                                if st.button("Like", key=like_key):
                                    # Saving liked series and refreshing page to apply changes
                                    save_liked_movie(series_id, title, series_genres, imdb_score, liked=True)
                                    st.success(f"Saved '{title}' to your preferences!")
                                    st.rerun()

                            with col_dislike:
                                if st.button("Dislike", key=dislike_key):
                                    # Saving disliked series and refreshing page to apply changes
                                    save_liked_movie(series_id, title, series_genres, imdb_score, liked=False)
                                    st.info(f"Noted that you don't like '{title}'")
                                    st.rerun()
                      
                        # Displaying series details
                        if poster_url:
                            st.image(poster_url, width=150)
                        st.markdown(f"IMDb Score: {imdb_score}")
                        st.caption(overview)
                        if trailer_url:
                            st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                        st.markdown("---")

        # Showing movies by favorite actor/director
        if prefs.get("favorite_person"):
            if content_type in ["Film"]:
                st.subheader(f"Movies featuring **{prefs['favorite_person']}**:")
                # Getting movies featuring this person
                person_movies = get_movies_by_actor_or_director(
                    prefs["favorite_person"],
                    runtime_min=runtime_min,
                    runtime_max=runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )

                # Re-ranking using Machine Learning if user has liked movies
                if liked_movies_list and person_movies:
                    # Applying ML-based reordering
                    person_movies = reorder_movies_by_preference(person_movies, liked_movies_list)
                    
                # Looping through each movie in the results to get needed data
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

                    # Creating header row with Like/Dislike buttons
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{title}** ({release_year})")
                    with col2:
                        like_key = f"like_person_{movie_id}"
                        dislike_key = f"dislike_person_{movie_id}"
                
                        col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                # Saving liked movies and refreshing page to apply changes
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()
                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                # Saving disliked movies and refreshing page to apply changes
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                 
                    # Displaying movie details
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")
            
            # Showing series by favorite actor/director
            if content_type in ["Series"]:
                st.subheader(f"Series featuring **{prefs['favorite_person']}**:")
                # Getting series featuring this person
                person_series = get_series_by_actor(
                    prefs["favorite_person"],
                    episode_runtime_min=episode_runtime_min,
                    episode_runtime_max=episode_runtime_max,
                    year_min=year_min,
                    year_max=year_max,
                    num_results=10
                )

                # Re-ranking using Machine Learning based on likes
                if liked_movies_list and person_series:
                    # Applying ML-based reordering
                    person_series = reorder_movies_by_preference(person_series, liked_movies_list)
                
                # Looping through each series in the results to get needed data
                for series in person_series:
                    title = series.get("name")
                    overview = series.get("overview", "No description available.")
                    poster_path = series.get("poster_path")
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
                    imdb_score = series.get("vote_average")
                    series_id = series.get("id")
                    first_air_year = series.get("first_air_date", "")[:4]
                    trailer_url = get_trailer(series_id, "tv")
                    series_genres = series.get("genre_ids", [])

                    # Creating header row with Like/Dislike buttons
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{title}** ({first_air_year})")
                    with col2:
                        like_key = f"like_person_series_{series_id}"
                        dislike_key = f"dislike_person_series_{series_id}"
                
                        col_like, col_dislike = st.columns(2)
                        with col_like:
                            if st.button("Like", key=like_key):
                                # Saving liked series and refreshing page to apply changes
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=True)
                                st.success(f"Saved '{title}' to your preferences!")
                                st.rerun()
                        with col_dislike:
                            if st.button("Dislike", key=dislike_key):
                                # Saving disliked series and refreshing page to apply changes
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=False)
                                st.info(f"Noted that you don't like '{title}'")
                                st.rerun()
                    
                    # Displaying series details
                    if poster_url:
                        st.image(poster_url, width=150)
                    st.markdown(f"IMDb Score: {imdb_score}")
                    st.caption(overview)
                    if trailer_url:
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
                    st.markdown("---")
        
        
        st.write("")
        # Creating button to restart and navigating back to step 1
        if st.button("Start Over"):
            goto("step1")
            st.rerun()

# RANDOM MOVIE MODE
# Random Movie page: displays a random popular movie with details
# Displaying page title
elif st.session_state.page == "random":
    st.title("Random Movie Generator")

    
    st.write("")
    # Creating back button with arrow and navigating back to step 1
    if st.button("← Back to Start"):
        goto("step1")
        st.rerun()
    
    # Creating refresh button to get a new random movie
    if st.button("Give me another random movie!"):
        st.rerun()
    
    # Getting and displaying random movie
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

        # Displaying movie details
        st.markdown(f"## {title} ({release_year})")
        if poster_url:
            st.image(poster_url, width=300)
        st.markdown(f"### IMDb Score: {rating}")
        st.markdown(f"Overview: {overview}")
        if trailer_url:
            st.markdown(f"### [Watch Trailer]({trailer_url})", unsafe_allow_html=True)
    else:
        # Getting movies failed so warning is showed
        st.warning("Could not fetch a random movie. Try again!")

# RYAN GOSLING MODE
# Ryan Gosling page: displays top-rated Ryan Gosling movies
# Displaying page title
elif st.session_state.page == "gosling":
    st.title("Ryan Gosling Recommendations")
    # Getting Ryan Gosling's top movies
    gosling_movies = get_ryan_gosling_movies()
    if gosling_movies:
        st.markdown("Sorted by IMDb Score (Highest First)")
        # Looping through each movie in the results to get needed data
        for movie in gosling_movies:
            title = movie.get("title")
            rating = movie.get("vote_average")
            overview = movie.get("overview", "No description available.")
            poster_path = movie.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None
            movie_id = movie.get("id")
            release_year = movie.get("release_date", "")[:4]
            trailer_url = get_trailer(movie_id, "movie")

            # Displaying movie details
            st.markdown(f"**{title}** ({release_year})")
            if poster_url:
                st.image(poster_url, width=150)
            st.markdown(f"IMDb Score: {rating}")
            st.caption(overview)
            if trailer_url:
                st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)
            st.markdown("---")
    else:
        # Getting movies failed so warning is showed
        st.warning("No Ryan Gosling movies found.")
    
    st.write("")
    # Creating back button and navigating back to step 1
    if st.button("← Back to Start"):
        goto("step1")
        st.rerun()
