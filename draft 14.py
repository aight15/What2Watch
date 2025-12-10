# Import necessary libraries for the application
import streamlit as st  # Web framework for creating the UI
import matplotlib.pyplot as plt  # Plotting library for creating the radar chart
import numpy as np  # Numerical operations library for arrays and math
import requests  # HTTP library for making API calls to TMDB
import random  # Random number generation for random movie feature
import json  # JSON parsing library for saving/loading user preferences
from sklearn.metrics.pairwise import cosine_similarity  # ML library for calculating similarity scores
from pathlib import Path  # File path handling library

# ------------------- PAGE SETUP -------------------
# Configure the Streamlit page with title and icon
st.set_page_config(page_title="What2Watch", page_icon="logo.jpg")  # Sets browser tab title and favicon

# ------------------- LOGO AND TITLE -------------------
# Create three columns with specific width ratios for centering the logo
col1, col2, col3 = st.columns([1, 3, 1])  # Creates layout with wider middle column
with col2:  # Use the middle column
    st.image("logo.jpg", width=700)  # Display the What2Watch logo centered

# Initialize page navigation state if not already set
if "page" not in st.session_state:  # Check if page state exists
    st.session_state.page = "step1"  # Set default starting page to step1

# ------------------- PAGE NAVIGATION -------------------
# Function to change the current page in the application
def goto(page_name):
    """Navigate to a different page by updating session state"""
    st.session_state.page = page_name  # Update the page state variable

# ------------------- SIDE BAR ---------------------
# Display sidebar instructions for the genre preference tool
st.sidebar.markdown("Uncertain which genre you like? Select below which movies and series you've enjoyed and figure out what your prefered genre is.")  # Show explanation text

# Define predefined lists of movies for genre analysis
movies = [
    "Pixels",  # Comedy/Sci-Fi/Action movie
    "The Conjuring",  # Horror movie
    "Blade Runner 2049",  # Sci-Fi/Drama/Action movie
    "The Shawshank Redemption",  # Drama movie
    "John Wick",  # Action movie
    "The Notebook"  # Drama/Romance movie
]

# Define predefined lists of TV series for genre analysis
series = [
    "Breaking Bad",  # Drama/Action series
    "Stranger Things",  # Horror/Sci-Fi/Action series
    "Friends",  # Comedy/Romance series
    "The Office",  # Comedy series
    "Game of Thrones",  # Drama/Action/Romance series
    "Black Mirror"  # Sci-Fi/Drama series
]

# Define the genre categories used in the radar chart
genres = ["Comedy", "Horror", "Sci-Fi", "Drama", "Action", "Romance"]  # List of all available genres

# Map each title to its genre composition (binary: 1 if title has genre, 0 if not)
title_genres = {
    "Pixels":               {"Comedy": 1, "Horror": 0, "Sci-Fi": 1, "Drama": 0, "Action": 1, "Romance": 0},  # Comedy/Sci-Fi/Action blend
    "The Conjuring":        {"Comedy": 0, "Horror": 1, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},  # Pure horror
    "Blade Runner 2049":    {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 1, "Romance": 0},  # Sci-Fi/Drama/Action
    "The Shawshank Redemption": {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 0},  # Pure drama
    "John Wick":            {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 1, "Romance": 0},  # Pure action
    "The Notebook":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 0, "Romance": 1},  # Drama/Romance

    "Breaking Bad":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 0},  # Drama/Action series
    "Stranger Things":      {"Comedy": 0, "Horror": 1, "Sci-Fi": 1, "Drama": 0, "Action": 1, "Romance": 0},  # Horror/Sci-Fi/Action series
    "Friends":              {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 1},  # Comedy/Romance series
    "The Office":           {"Comedy": 1, "Horror": 0, "Sci-Fi": 0, "Drama": 0, "Action": 0, "Romance": 0},  # Pure comedy series
    "Game of Thrones":      {"Comedy": 0, "Horror": 0, "Sci-Fi": 0, "Drama": 1, "Action": 1, "Romance": 1},  # Drama/Action/Romance series
    "Black Mirror":         {"Comedy": 0, "Horror": 0, "Sci-Fi": 1, "Drama": 1, "Action": 0, "Romance": 0},  # Sci-Fi/Drama series
}

# Create empty list to store user's selected titles
selected_titles = []  # Will be populated based on checkbox selections

# Display movie checkboxes in sidebar
st.sidebar.markdown("#### Movies")  # Section header for movies
for m in movies:  # Loop through each movie in the list
    if st.sidebar.checkbox(m, key=f"movie_{m}"):  # Create checkbox with unique key for each movie
        selected_titles.append(m)  # Add movie to selected list if checked

# Display series checkboxes in sidebar
st.sidebar.markdown("#### Series")  # Section header for series
for s in series:  # Loop through each series in the list
    if st.sidebar.checkbox(s, key=f"series_{s}"):  # Create checkbox with unique key for each series
        selected_titles.append(s)  # Add series to selected list if checked

# --- CALCULATE GENRE SCORES ---
# Initialize all genre scores to zero
genre_scores = {g: 0 for g in genres}  # Creates dictionary with each genre set to 0

# Calculate total score for each genre based on selected titles
for title in selected_titles:  # Loop through each title user selected
    for g in genres:  # Loop through each genre
        genre_scores[g] += title_genres[title][g]  # Add genre value from title to total score

# Prepare values for radar chart by extracting scores in order
values = [genre_scores[g] for g in genres]  # Convert dictionary to ordered list
values += values[:1]  # Duplicate first value at end to close the radar chart polygon

# --- RADAR CHART ---
# Calculate number of genre axes for the chart
num_vars = len(genres)  # Count of genres (6)

# Calculate angle for each axis in radians
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()  # Evenly space angles around circle
angles += angles[:1]  # Duplicate first angle to close the chart

# Create polar subplot for radar chart
fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))  # Create 4x4 inch polar plot

# Plot the genre scores as a line on the radar chart
ax.plot(angles, values, linewidth=2)  # Draw line connecting all points
# Fill the area inside the radar chart polygon
ax.fill(angles, values, alpha=0.25)  # Fill with 25% opacity

# Set the position and labels for each axis
ax.set_xticks(angles[:-1])  # Set tick positions (exclude duplicate)
ax.set_xticklabels(genres)  # Label each axis with genre name
ax.set_rlabel_position(30)  # Rotate radial labels 30 degrees

# Display the radar chart in the sidebar
st.sidebar.pyplot(fig)  # Render matplotlib figure in Streamlit

# ------------------- TMDB SETUP -------------------
# TMDB API configuration
TMDB_API_KEY = "ef26791dfc9c3b8254044fe9167e3edb"  # API key for authenticating with TMDB
TMDB_BASE_URL = "https://api.themoviedb.org/3"  # Base URL for all TMDB API endpoints

# Map genre names to TMDB genre IDs FOR MOVIES
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

# Map genre names to TMDB genre IDs FOR TV SERIES
TV_GENRE_MAP = {
    "Action": 10759,      # Action & Adventure
    "Comedy": 35,
    "Drama": 18,
    "Sci-Fi": 10765,      # Sci-Fi & Fantasy
    "Documentary": 99,
    "Animation": 16,
    "Mystery": 9648,
    "Crime": 80
}

# ------------------- TMDB API FUNCTIONS -------------------
# Function to fetch movies from TMDB based on genre and various filters
def get_movies_by_genre(genre_name, popularity_type="popular", animation_filter=None, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches movies from TMDB by genre with optional filters for popularity, animation, runtime and release year"""
    genre_id = MOVIE_GENRE_MAP.get(genre_name)  # Use MOVIE_GENRE_MAP
    if not genre_id:
        return []
    
    url = f"{TMDB_BASE_URL}/discover/movie"  # Build URL for movie discovery endpoint
    # Set up query parameters for the API request
    params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "with_genres": genre_id,  # Filter by genre ID
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",  # Sort by popularity or rating
        "language": "en-US",  # Request English language results
        "vote_count.gte": 100 if popularity_type == "popular" else 50  # Minimum votes filter (higher for popular)
    }

    # Apply animation filter if specified
    if animation_filter == "Animated":  # User wants only animated content
        params["with_genres"] = f"{genre_id},16"  # Add animation genre ID (16) to filter
    elif animation_filter == "Live-action":  # User wants only live-action content
        params["without_genres"] = "16"  # Exclude animation genre

    # Apply runtime filters if specified
    if runtime_min:  # User specified minimum runtime
        params["with_runtime.gte"] = runtime_min  # Greater than or equal to min runtime
    if runtime_max:  # User specified maximum runtime
        params["with_runtime.lte"] = runtime_max  # Less than or equal to max runtime
    
    # Apply year filters if specified
    if year_min:  # User specified earliest year
        params["primary_release_date.gte"] = f"{year_min}-01-01"  # Format as date (Jan 1)
    if year_max:  # User specified latest year
        params["primary_release_date.lte"] = f"{year_max}-12-31"  # Format as date (Dec 31)

    # Make the API request
    response = requests.get(url, params=params)  # Send GET request to TMDB
    if response.status_code == 200:  # Check if request was successful
        return response.json().get("results", [])[:num_results]  # Return first num_results movies
    return []  # Return empty list if request failed

# Function to fetch TV series from TMDB based on genre and various filters
def get_series_by_genre(genre_name, popularity_type="popular", animation_filter=None, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches TV series from TMDB by genre with optional filters for popularity, animation and air date"""
    genre_id = TV_GENRE_MAP.get(genre_name)  # Use TV_GENRE_MAP
    if not genre_id:
        return []
    
    url = f"{TMDB_BASE_URL}/discover/tv"  # Build URL for TV discovery endpoint
    # Set up query parameters for the API request
    params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "with_genres": genre_id,  # Filter by genre ID
        "sort_by": "popularity.desc" if popularity_type == "popular" else "vote_average.desc",  # Sort by popularity or rating
        "language": "en-US",  # Request English language results
        "vote_count.gte": 50  # Minimum votes filter
    }

    # Apply animation filter if specified
    if animation_filter == "Animated":  # User wants only animated content
        params["with_genres"] = f"{genre_id},16"  # Add animation genre ID (16) to filter
    elif animation_filter == "Live-action":  # User wants only live-action content
        params["without_genres"] = "16"  # Exclude animation genre
    
    # Apply year filters if specified
    if year_min:  # User specified earliest air date
        params["first_air_date.gte"] = f"{year_min}-01-01"  # Format as date (Jan 1)
    if year_max:  # User specified latest air date
        params["first_air_date.lte"] = f"{year_max}-12-31"  # Format as date (Dec 31)

    # Make the API request
    response = requests.get(url, params=params)  # Send GET request to TMDB
    if response.status_code == 200:  # Check if request was successful
        return response.json().get("results", [])[:num_results]  # Return first num_results series
    return []  # Return empty list if request failed

# Function to fetch movies featuring or directed by a specific person
def get_movies_by_actor_or_director(name, runtime_min=None, runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches movies from TMDB featuring or directed by a person, with optional filters for runtime and release year"""
    # First, search for the person by name
    search_url = f"{TMDB_BASE_URL}/search/person"  # Build URL for person search endpoint
    search_params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "query": name,  # Person's name to search for
        "language": "en-US"  # Request English language results
    }
    response = requests.get(search_url, params=search_params)  # Send GET request to search for person
    if response.status_code == 200 and response.json()["results"]:  # Check if search was successful and has results
        person_id = response.json()["results"][0]["id"]  # Get the ID of the first matching person
        # Now search for movies featuring this person
        discover_url = f"{TMDB_BASE_URL}/discover/movie"  # Build URL for movie discovery endpoint
        discover_params = {
            "api_key": TMDB_API_KEY,  # Authentication key
            "with_cast": person_id,  # Filter by person ID in cast
            "sort_by": "popularity.desc",  # Sort by popularity
            "vote_count.gte": 50,  # Minimum votes filter
            "language": "en-US"  # Request English language results
        }
        
        # Apply runtime filters if specified
        if runtime_min:  # User specified minimum runtime
            discover_params["with_runtime.gte"] = runtime_min  # Greater than or equal to min runtime
        if runtime_max:  # User specified maximum runtime
            discover_params["with_runtime.lte"] = runtime_max  # Less than or equal to max runtime
        # Apply year filters if specified
        if year_min:  # User specified earliest year
            discover_params["primary_release_date.gte"] = f"{year_min}-01-01"  # Format as date (Jan 1)
        if year_max:  # User specified latest year
            discover_params["primary_release_date.lte"] = f"{year_max}-12-31"  # Format as date (Dec 31)
        
        # Make the API request for movies
        movie_response = requests.get(discover_url, params=discover_params)  # Send GET request to TMDB
        if movie_response.status_code == 200:  # Check if request was successful
            return movie_response.json().get("results", [])[:num_results]  # Return first num_results movies
    return []  # Return empty list if search or request failed

# Function to fetch TV series featuring a specific actor
def get_series_by_actor(name, episode_runtime_min=None, episode_runtime_max=None, year_min=None, year_max=None, num_results=10):
    """Fetches TV series from TMDB featuring a given actor, with optional filters for first air date"""
    # First, search for the person by name
    search_url = f"{TMDB_BASE_URL}/search/person"  # Build URL for person search endpoint
    search_params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "query": name,  # Person's name to search for
        "language": "en-US"  # Request English language results
    }
    response = requests.get(search_url, params=search_params)  # Send GET request to search for person
    if response.status_code == 200 and response.json()["results"]:  # Check if search was successful and has results
        person_id = response.json()["results"][0]["id"]  # Get the ID of the first matching person
        # Now search for TV series featuring this person
        discover_url = f"{TMDB_BASE_URL}/discover/tv"  # Build URL for TV discovery endpoint
        discover_params = {
            "api_key": TMDB_API_KEY,  # Authentication key
            "with_cast": person_id,  # Filter by person ID in cast
            "sort_by": "popularity.desc",  # Sort by popularity
            "vote_count.gte": 30,  # Minimum votes filter (lower for TV)
            "language": "en-US"  # Request English language results
        }
        
        # Apply year filters if specified
        if year_min:  # User specified earliest air date
            discover_params["first_air_date.gte"] = f"{year_min}-01-01"  # Format as date (Jan 1)
        if year_max:  # User specified latest air date
            discover_params["first_air_date.lte"] = f"{year_max}-12-31"  # Format as date (Dec 31)
        
        # Make the API request for series
        series_response = requests.get(discover_url, params=discover_params)  # Send GET request to TMDB
        if series_response.status_code == 200:  # Check if request was successful
            return series_response.json().get("results", [])[:num_results]  # Return first num_results series
    return []  # Return empty list if search or request failed

# Function to fetch Ryan Gosling's top-rated movies
def get_ryan_gosling_movies():
    """Fetches the top 10 highest-rated Ryan Gosling movies from TMDB, sorted by average vote"""
    # First, search for Ryan Gosling
    search_url = f"{TMDB_BASE_URL}/search/person"  # Build URL for person search endpoint
    search_params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "query": "Ryan Gosling",  # Hardcoded search for Ryan Gosling
        "language": "en-US"  # Request English language results
    }
    person_response = requests.get(search_url, params=search_params)  # Send GET request to search for Ryan Gosling
    if person_response.status_code == 200 and person_response.json()['results']:  # Check if search was successful
        gosling_id = person_response.json()['results'][0]['id']  # Get Ryan Gosling's TMDB ID
        # Now get movies featuring Ryan Gosling
        movie_url = f"{TMDB_BASE_URL}/discover/movie"  # Build URL for movie discovery endpoint
        movie_params = {
            "api_key": TMDB_API_KEY,  # Authentication key
            "with_cast": gosling_id,  # Filter by Ryan Gosling's ID
            "sort_by": "vote_count.desc",  # Sort by number of votes initially
            "vote_count.gte": 50,  # Minimum votes filter
            "language": "en-US"  # Request English language results
        }
        movie_response = requests.get(movie_url, params=movie_params)  # Send GET request to TMDB
        if movie_response.status_code == 200:  # Check if request was successful
            movies = movie_response.json().get("results", [])  # Get list of movies
            sorted_movies = sorted(movies, key=lambda x: x.get("vote_average", 0), reverse=True)  # Sort by rating (highest first)
            return sorted_movies[:10]  # Return top 10 highest-rated movies
    return []  # Return empty list if search or request failed

# Function to get a random popular movie
def get_random_movie():
    """Get a truly random popular movie by selecting a random results page and movie"""
    random_page = random.randint(1, 50)  # Generate random page number between 1 and 50
    url = f"{TMDB_BASE_URL}/movie/popular"  # Build URL for popular movies endpoint
    params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "language": "en-US",  # Request English language results
        "page": random_page  # Use the random page number
    }
    response = requests.get(url, params=params)  # Send GET request to TMDB
    if response.status_code == 200:  # Check if request was successful
        results = response.json().get("results", [])  # Get list of movies from that page
        if results:  # If page has results
            return random.choice(results)  # Return a random movie from the page
    return None  # Return None if request failed or no results

# Function to fetch trailer URL for a movie or TV show
def get_trailer(content_id, content_type="movie"):
    """Fetches the YouTube trailer URL for a given movie or TV show from TMDB"""
    url = f"{TMDB_BASE_URL}/{content_type}/{content_id}/videos"  # Build URL for videos endpoint
    params = {
        "api_key": TMDB_API_KEY,  # Authentication key
        "language": "en-US"  # Request English language results
    }
    response = requests.get(url, params=params)  # Send GET request to TMDB
    if response.status_code == 200:  # Check if request was successful
        videos = response.json().get("results", [])  # Get list of videos
        for video in videos:  # Loop through each video
            if video["site"] == "YouTube" and video["type"] == "Trailer":  # Check if it's a YouTube trailer
                return f"https://www.youtube.com/watch?v={video['key']}"  # Return YouTube URL
    return None  # Return None if no trailer found


# ------------------- MACHINE LEARNING COMPONENT -------------------
# Function to load user's liked movies from JSON file
def load_liked_movies():
    """Load user's liked movies from JSON file"""
    try:  # Try to load the file
        if Path("liked_movies.json").exists():  # Check if file exists
            with open("liked_movies.json", "r") as f:  # Open file for reading
                data = json.load(f)  # Parse JSON data
                # Filter out invalid entries (strings, etc.)
                return [m for m in data if isinstance(m, dict) and "id" in m and m.get("liked") == True]  # Return only valid liked movies
        return []  # Return empty list if file doesn't exist
    except (FileNotFoundError, json.JSONDecodeError):  # Catch file or JSON errors
        return []  # Return empty list if error occurs

# Function to save a liked or disliked movie to the JSON file
def save_liked_movie(movie_id, title, genres, rating, liked=True):
    """Save a liked/disliked movie to the JSON file"""
    try:  # Try to save the data
        if Path("liked_movies.json").exists():  # Check if file exists
            with open("liked_movies.json", "r") as f:  # Open file for reading
                data = json.load(f)  # Parse existing JSON data
                # Filter out invalid entries
                data = [m for m in data if isinstance(m, dict) and "id" in m]  # Keep only valid entries
        else:  # File doesn't exist
            data = []  # Start with empty list
        
        # Remove existing entry for this movie if present
        data = [m for m in data if m.get("id") != movie_id]  # Filter out this movie ID
        
        # Add new entry
        data.append({
            "id": movie_id,  # Movie's TMDB ID
            "title": title,  # Movie title
            "genres": genres,  # List of genre IDs
            "rating": rating,  # IMDb score
            "liked": liked  # Whether user liked (True) or disliked (False)
        })
        
        # Save updated data to file
        with open("liked_movies.json", "w") as f:  # Open file for writing
            json.dump(data, f, indent=2)  # Write JSON with pretty formatting
    except Exception as e:  # Catch any errors
        st.error(f"Error saving preference: {e}")  # Display error message to user

# Function to create a feature vector for machine learning
def create_movie_feature_vector(movie):
    """Create a feature vector for a movie based on genres, rating, and popularity"""
    # Get all possible genre IDs from both MOVIE_GENRE_MAP and TV_GENRE_MAP
    all_genre_ids = list(set(list(MOVIE_GENRE_MAP.values()) + list(TV_GENRE_MAP.values())))
    
    # Create genre vector (binary: 1 if movie has genre, 0 otherwise)
    movie_genres = movie.get("genre_ids", [])  # Get list of genre IDs for this movie
    genre_vector = [1 if genre_id in movie_genres else 0 for genre_id in all_genre_ids]  # Create binary vector
    
    # Normalize rating (0-10 scale, normalize to 0-1)
    rating = movie.get("vote_average", 5.0) / 10.0  # Divide by 10 to get value between 0 and 1
    
    # Normalize popularity (using a simple log transform to reduce scale)
    popularity = movie.get("popularity", 0)  # Get popularity score
    popularity_normalized = np.log1p(popularity) / 20.0  # Apply log transform and scale down
    
    # Combine all features into single vector
    feature_vector = genre_vector + [rating, popularity_normalized]  # Concatenate genre, rating, popularity
    return np.array(feature_vector)  # Convert to numpy array for ML operations

# Function to reorder movies based on user preferences using ML
def reorder_movies_by_preference(movies, liked_movies_list):
    """Re-order movies based on similarity to user's liked movies using cosine similarity"""
    if not liked_movies_list or not movies:  # Check if we have data to work with
        return movies  # Return original order if no liked movies or no movies to sort
    
    # Create feature vectors for liked movies
    liked_vectors = []  # Initialize empty list for vectors
    for liked_movie in liked_movies_list:  # Loop through each liked movie
        # Reconstruct movie dict from saved data
        movie_dict = {
            "genre_ids": liked_movie.get("genres", []),  # Get saved genre IDs
            "vote_average": liked_movie.get("rating", 5.0),  # Get saved rating
            "popularity": 50.0  # Default popularity if not stored
        }
        liked_vectors.append(create_movie_feature_vector(movie_dict))  # Create and add feature vector
    
    if not liked_vectors:  # Check if we successfully created vectors
        return movies  # Return original order if no vectors created
    
    # Average the liked movie vectors to create a user preference profile
    user_profile = np.mean(liked_vectors, axis=0)  # Calculate mean of all liked movie vectors
    
    # Calculate similarity scores for candidate movies
    movie_scores = []  # Initialize empty list for movie-score pairs
    for movie in movies:  # Loop through each candidate movie
        movie_vector = create_movie_feature_vector(movie)  # Create feature vector for this movie
        # Calculate cosine similarity between user profile and movie
        similarity = cosine_similarity([user_profile], [movie_vector])[0][0]  # Get similarity score (0-1)
        movie_scores.append((movie, similarity))  # Add movie and its score to list
    
    # Sort by similarity (highest first)
    movie_scores.sort(key=lambda x: x[1], reverse=True)  # Sort by second element (similarity) descending
    
    # Return reordered movies
    return [movie for movie, score in movie_scores]  # Extract just the movies in sorted order

# Initialize preferences dictionary in session state
if "preferences" not in st.session_state:  # Check if preferences exists in session
    st.session_state.preferences = {}  # Create empty dictionary for storing user preferences

# Function to display centered buttons for special features
def special_buttons():
    """Displays centered/symmetrical buttons in Streamlit to navigate to Random Movie or Ryan Gosling pages"""
    col1, col2, col3 = st.columns([2, 3, 2])  # Create three columns with specific width ratios
    with col1:  # Use left column
        if st.button("Random Movie", key="random_btn", use_container_width=True):  # Create full-width button
            goto("random")  # Navigate to random movie page
            st.rerun()
    with col3:  # Use right column
        if st.button("Ryan Gosling", key="gosling_btn", use_container_width=True):  # Create full-width button
            goto("gosling")  # Navigate to Ryan Gosling page
            st.rerun()

# ------------------- STEP 1 -------------------
# Step 1 of the form: asks user for content type
if st.session_state.page == "step1":  # Check if current page is step1
    special_buttons()  # Display Random Movie and Ryan Gosling buttons
    st.title("What2Watch")  # Display main title
    with st.form("step1_form"):  # Create form to group inputs
        content_type = st.radio("Do you want to watch a movie, series, or both?", ["Film", "Series", "Both"])  # Radio buttons for content type
        next_button = st.form_submit_button("Next")  # Submit button
    if next_button:  # Check if user clicked Next
        st.session_state.preferences["content_type"] = content_type  # Save content type to session
        goto("step2")  # Navigate to step 2
        st.rerun()

# ------------------- STEP 2 -------------------
# Step 2 of the form: collects all user preferences
elif st.session_state.page == "step2":  # Check if current page is step2
    special_buttons()  # Display Random Movie and Ryan Gosling buttons
    with st.form("step2_form"):  # Create form to group inputs
        content_type = st.session_state.preferences.get("content_type", "Film")  # Get content type from session
        
        # Length preference - varies based on content type
        if content_type == "Film":  # User wants only movies
            length = st.radio("Preferred movie length:", ["Short (< 90 min)", "Medium (90–120 min)", "Long (> 120 min)", "Any length"])  # Movie length options
        elif content_type == "Series":  # User wants only series
            length = st.radio("Preferred episode length:", ["< 30 min", "30–60 min", "60+ min", "Any length"])  # Episode length options
        else:  # User wants both movies and series
            length = st.radio("Preferred duration:", [
                "Short Movie (< 90 min)",  # Short movie option
                "Medium Movie (90–120 min)",  # Medium movie option
                "Long Movie (> 120 min)",  # Long movie option
                "Short Episode (< 30 min)",  # Short episode option
                "Standard Episode (30–60 min)",  # Standard episode option
                "Long Episode (> 60 min)",  # Long episode option
                "Any length"  # No preference option
            ])

        # Animation preference
        animation_preference = st.radio("Would you prefer animated or live-action?", ["Animated", "Live-action", "Both"])  # Radio buttons for animation type
        
        # Modern or classic preference
        modern_or_classic = st.radio("Modern or classic?", ["Modern (2010+)", "Classic (before 2010)", "Doesn't matter"])  # Radio buttons for era preference
        
        # Genre selection with preferred genre hint
        # Determine preferred genre from sidebar if any titles selected
        preferred_genre_text = ""  # Initialize empty string for genre hint
        if selected_titles:  # Check if user selected any titles in sidebar
            max_score = max(genre_scores.values())  # Find highest genre score
            if max_score > 0:  # Check if any genre has a score
                top_genres = [g for g, score in genre_scores.items() if score == max_score]  # Get all genres with max score
                if len(top_genres) == 1:  # Only one top genre
                    preferred_genre_text = f"(Your preferred genre is **{top_genres[0]}**)"  # Show singular message
                else:  # Multiple top genres
                    preferred_genre_text = f"(Your preferred genres are **{', '.join(top_genres)}**)"  # Show plural message with comma-separated list
        
        st.markdown(f"**Which genre are you interested in?** {preferred_genre_text}")  # Display question with genre hint
        if content_type == "Film":  # User wants only movies
             genre_choice = st.multiselect("", options=list(MOVIE_GENRE_MAP.keys()), label_visibility="collapsed")  # Multi-select dropdown for genres (hidden label)
        elif content_type == "Series":  # User wants only series
            genre_choice = st.multiselect("", options=list(TV_GENRE_MAP.keys()), label_visibility="collapsed")  # Multi-select dropdown for genres (hidden label)
       

        # Popularity type preference
        popularity_type = st.radio("Do you want a well-known hit or a hidden gem?", ["Popular & trending", "Underrated", "Both"])  # Radio buttons for popularity

        # Actor/director input (optional)
        actor_or_director = st.text_input("Any actors or directors you love? (optional)")  # Text input for favorite person

        # Navigation buttons in two columns
        col1, col2 = st.columns(2)  # Create two equal columns
        with col1:  # Left column
            back_button = st.form_submit_button("Back")  # Back button
        with col2:  # Right column
            next_button = st.form_submit_button("Next")  # Next button

    # Handle button clicks
    if next_button:  # User clicked Next
        st.session_state.preferences.update({  # Update preferences dictionary with all selections
            "length": length,  # Save length preference
            "animation_preference": animation_preference,  # Save animation preference
            "modern_or_classic": modern_or_classic,  # Save era preference
            "genres": genre_choice,  # Save selected genres
            "popularity_type": popularity_type,  # Save popularity preference
            "favorite_person": actor_or_director  # Save favorite actor/director
        })
        goto("results")  # Navigate to results page
        st.rerun()
    elif back_button:  # User clicked Back
        goto("step1")  # Navigate back to step 1
        st.rerun()

# ------------------- RESULTS -------------------
# Results page: displays personalized movie and series recommendations
elif st.session_state.page == "results":  # Check if current page is results
    prefs = st.session_state.preferences  # Get all preferences from session
    content_type = prefs.get("content_type", "Film")  # Get content type (default to Film)
    
    # Validate that user selected at least one genre
    if not prefs.get("genres"):  # Check if genres list is empty
        st.warning("Please go back and select at least one genre.")  # Show warning message
    else:  # User selected genres, proceed with recommendations
        # Parse length preferences for runtime filtering
        runtime_min, runtime_max = None, None  # Initialize movie runtime variables
        episode_runtime_min, episode_runtime_max = None, None  # Initialize episode runtime variables
        
        length = prefs.get("length", "")  # Get length preference from session
        
        # Map length preferences to runtime filter values for movies
        if "Short (< 90 min)" in length or "Short Movie" in length:  # User wants short movies
            runtime_max = 90  # Set maximum runtime to 90 minutes
        elif "Medium (90–120 min)" in length or "Medium Movie" in length:  # User wants medium movies
            runtime_min, runtime_max = 90, 120  # Set runtime range 90-120 minutes
        elif "Long (> 120 min)" in length or "Long Movie" in length:  # User wants long movies
            runtime_min = 120  # Set minimum runtime to 120 minutes
        # Map length preferences to runtime filter values for series
        elif "< 30 min" in length or "Short Episode" in length:  # User wants short episodes
            episode_runtime_max = 30  # Set maximum episode runtime to 30 minutes
        elif "30–60 min" in length or "Standard Episode" in length:  # User wants standard episodes
            episode_runtime_min, episode_runtime_max = 30, 60  # Set episode runtime range 30-60 minutes
        elif "60+ min" in length or "Long Episode" in length:  # User wants long episodes
            episode_runtime_min = 60  # Set minimum episode runtime to 60 minutes
        
        # Parse year preferences for filtering by release/air date
        year_min, year_max = None, None  # Initialize year filter variables
        modern_or_classic = prefs.get("modern_or_classic", "Doesn't matter")  # Get era preference
        if modern_or_classic == "Modern (2010+)":  # User wants modern content
            year_min = 2010  # Set minimum year to 2010
        elif modern_or_classic == "Classic (before 2010)":  # User wants classic content
            year_max = 2009  # Set maximum year to 2009
        
        # Determine popularity type for API calls
        pop_type = "popular" if prefs["popularity_type"] == "Popular & trending" else "underrated"  # Map UI choice to API parameter

        # Load liked movies for personalization with Machine Learning
        liked_movies_list = load_liked_movies()  # Load user's liked movies from JSON file
        
        # Show Movies section
        if content_type in ["Film", "Both"]:  # Check if user wants movie recommendations
            st.subheader("Recommended Movies:")  # Display section header

            # Show personalization info if user has liked movies
            if liked_movies_list:  # Check if user has any liked movies
                st.info(f"Personalizing recommendations based on {len(liked_movies_list)} liked movie(s)!")  # Display info message
            
            # Loop through each selected genre
            for genre in prefs["genres"]:  # Iterate through user's selected genres
                # Fetch movies from TMDB API (now passing genre name instead of ID)
                movies = get_movies_by_genre(
                    genre,  # Genre name (not ID)
                    popularity_type=pop_type,  # Popular or underrated
                    animation_filter=prefs.get("animation_preference"),  # Animated/Live-action/Both
                    runtime_min=runtime_min,  # Minimum runtime
                    runtime_max=runtime_max,  # Maximum runtime
                    year_min=year_min,  # Earliest release year
                    year_max=year_max,  # Latest release year
                    num_results=10  # Number of results to fetch
                )

                if not movies:  # Check if API returned any movies
                    continue  # Skip to next genre if no movies found

                # Re-rank movies using Machine Learning if user has liked movies
                if liked_movies_list:  # Check if personalization data exists
                    movies = reorder_movies_by_preference(movies, liked_movies_list)  # Apply ML-based reordering
                
                st.markdown(f"### {genre}")  # Display genre header
                # Loop through each movie in the results
                for movie in movies:  # Iterate through movie list
                    title = movie.get("title")  # Get movie title
                    overview = movie.get("overview", "No description available.")  # Get overview (with default)
                    poster_path = movie.get("poster_path")  # Get poster image path
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None  # Build full poster URL if path exists
                    imdb_score = movie.get("vote_average")  # Get IMDb rating
                    movie_id = movie.get("id")  # Get TMDB movie ID
                    release_year = movie.get("release_date", "")[:4]  # Extract year from release date (first 4 characters)
                    trailer_url = get_trailer(movie_id, "movie")  # Fetch trailer URL
                    movie_genres = movie.get("genre_ids",[])  # Get list of genre IDs for this movie

                    # Create header row with Like/Dislike buttons
                    col1,col2 = st.columns([3,1])  # Create two columns (3:1 ratio)
                    with col1:  # Left column for title
                        st.markdown(f"**{title}** ({release_year})")  # Display bold title with year
                    with col2:  # Right column for buttons
                        like_key = f"like_{movie_id}_{genre}"  # Create unique key for Like button
                        dislike_key = f"dislike_{movie_id}_{genre}"  # Create unique key for Dislike button

                        col_like, col_dislike = st.columns(2)  # Create two sub-columns for buttons
                    with col_like:  # Like button column
                        if st.button("Like", key=like_key):  # Create Like button
                            save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)  # Save as liked movie
                            st.success(f"Saved '{title}' to your preferences!")  # Show success message
                            st.rerun()  # Refresh page to apply changes
                    with col_dislike:  # Dislike button column
                        if st.button("Dislike", key=dislike_key):  # Create Dislike button
                            save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)  # Save as disliked movie
                            st.info(f"Noted that you don't like '{title}'")  # Show info message
                            st.rerun()  # Refresh page to apply changes
                    
                    # Display movie details
                    if poster_url:  # Check if poster URL exists
                        st.image(poster_url, width=150)  # Display poster image
                    st.markdown(f"IMDb Score: {imdb_score}")  # Display rating
                    st.caption(overview)  # Display movie overview
                    if trailer_url:  # Check if trailer URL exists
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link
                    st.markdown("---")  # Display horizontal divider
        
        # Show Series section
        if content_type in ["Series", "Both"]:  # Check if user wants series recommendations
            st.subheader("Recommended Series:")  # Display section header
            # Loop through each selected genre
            for genre in prefs["genres"]:  # Iterate through user's selected genres
                # Fetch series from TMDB API (now passing genre name instead of ID)
                series_list = get_series_by_genre(
                    genre,  # Genre name (not ID)
                    popularity_type=pop_type,  # Popular or underrated
                    animation_filter=prefs.get("animation_preference"),  # Animated/Live-action/Both
                    episode_runtime_min=episode_runtime_min,  # Minimum episode runtime
                    episode_runtime_max=episode_runtime_max,  # Maximum episode runtime
                    year_min=year_min,  # Earliest air date
                    year_max=year_max,  # Latest air date
                    num_results=10  # Number of results to fetch
                )

                # Re-rank using Machine Learning
                if liked_movies_list and series_list:  # Check if personalization data and results exist
                    series_list = reorder_movies_by_preference(series_list, liked_movies_list)  # Apply ML-based reordering

                if series_list:  # Check if API returned any series
                    st.markdown(f"### {genre}")  # Display genre header
                    # Loop through each series in the results
                    for series in series_list:  # Iterate through series list
                        title = series.get("name")  # Get series name (note: "name" not "title" for TV)
                        overview = series.get("overview", "No description available.")  # Get overview (with default)
                        poster_path = series.get("poster_path")  # Get poster image path
                        poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None  # Build full poster URL if path exists
                        imdb_score = series.get("vote_average")  # Get IMDb rating
                        series_id = series.get("id")  # Get TMDB series ID
                        first_air_year = series.get("first_air_date", "")[:4]  # Extract year from first air date (first 4 characters)
                        trailer_url = get_trailer(series_id, "tv")  # Fetch trailer URL (note: content_type="tv")
                        series_genres = series.get("genre_ids", [])  # Get list of genre IDs for this series
                        
                        # Create header row with Like/Dislike buttons
                        col1, col2 = st.columns([3, 1])  # Create two columns (3:1 ratio)
                        with col1:  # Left column for title
                            st.markdown(f"**{title}** ({first_air_year})")  # Display bold title with year
                        with col2:  # Right column for buttons
                            like_key = f"like_series_{series_id}_{genre}"  # Create unique key for Like button
                            dislike_key = f"dislike_series_{series_id}_{genre}"  # Create unique key for Dislike button

                            col_like, col_dislike = st.columns(2)  # Create two sub-columns for buttons
                            with col_like:  # Like button column
                                if st.button("Like", key=like_key):  # Create Like button
                                    save_liked_movie(series_id, title, series_genres, imdb_score, liked=True)  # Save as liked series
                                    st.success(f"Saved '{title}' to your preferences!")  # Show success message
                                    st.rerun()  # Refresh page to apply changes

                            with col_dislike:  # Dislike button column
                                if st.button("Dislike", key=dislike_key):  # Create Dislike button
                                    save_liked_movie(series_id, title, series_genres, imdb_score, liked=False)  # Save as disliked series
                                    st.info(f"Noted that you don't like '{title}'")  # Show info message
                                    st.rerun()  # Refresh page to apply changes
                      
                        # Display series details
                        if poster_url:  # Check if poster URL exists
                            st.image(poster_url, width=150)  # Display poster image
                        st.markdown(f"IMDb Score: {imdb_score}")  # Display rating
                        st.caption(overview)  # Display series overview
                        if trailer_url:  # Check if trailer URL exists
                            st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link
                        st.markdown("---")  # Display horizontal divider

        # Show content by favorite actor/director section
        if prefs.get("favorite_person"):  # Check if user entered a favorite actor/director
            # Movies by favorite person
            if content_type in ["Film", "Both"]:  # Check if user wants movie recommendations
                st.subheader(f"Movies featuring **{prefs['favorite_person']}**:")  # Display section header with person's name
                # Fetch movies featuring this person
                person_movies = get_movies_by_actor_or_director(
                    prefs["favorite_person"],  # Person's name
                    runtime_min=runtime_min,  # Minimum runtime
                    runtime_max=runtime_max,  # Maximum runtime
                    year_min=year_min,  # Earliest release year
                    year_max=year_max,  # Latest release year
                    num_results=10  # Number of results to fetch
                )

                # Re-rank using Machine Learning if user has liked movies
                if liked_movies_list and person_movies:  # Check if personalization data and results exist
                    person_movies = reorder_movies_by_preference(person_movies, liked_movies_list)  # Apply ML-based reordering
                    
                # Loop through each movie in the results
                for movie in person_movies:  # Iterate through movie list
                    title = movie.get("title")  # Get movie title
                    overview = movie.get("overview", "No description available.")  # Get overview (with default)
                    poster_path = movie.get("poster_path")  # Get poster image path
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None  # Build full poster URL if path exists
                    imdb_score = movie.get("vote_average")  # Get IMDb rating
                    movie_id = movie.get("id")  # Get TMDB movie ID
                    release_year = movie.get("release_date", "")[:4]  # Extract year from release date (first 4 characters)
                    trailer_url = get_trailer(movie_id, "movie")  # Fetch trailer URL
                    movie_genres = movie.get("genre_ids", [])  # Get list of genre IDs for this movie

                    # Create header row with Like/Dislike buttons
                    col1, col2 = st.columns([3, 1])  # Create two columns (3:1 ratio)
                    with col1:  # Left column for title
                        st.markdown(f"**{title}** ({release_year})")  # Display bold title with year
                    with col2:  # Right column for buttons
                        like_key = f"like_person_{movie_id}"  # Create unique key for Like button
                        dislike_key = f"dislike_person_{movie_id}"  # Create unique key for Dislike button
                
                        col_like, col_dislike = st.columns(2)  # Create two sub-columns for buttons
                        with col_like:  # Like button column
                            if st.button("Like", key=like_key):  # Create Like button
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=True)  # Save as liked movie
                                st.success(f"Saved '{title}' to your preferences!")  # Show success message
                                st.rerun()  # Refresh page to apply changes
                        with col_dislike:  # Dislike button column
                            if st.button("Dislike", key=dislike_key):  # Create Dislike button
                                save_liked_movie(movie_id, title, movie_genres, imdb_score, liked=False)  # Save as disliked movie
                                st.info(f"Noted that you don't like '{title}'")  # Show info message
                                st.rerun()  # Refresh page to apply changes
                 
                    # Display movie details
                    if poster_url:  # Check if poster URL exists
                        st.image(poster_url, width=150)  # Display poster image
                    st.markdown(f"IMDb Score: {imdb_score}")  # Display rating
                    st.caption(overview)  # Display movie overview
                    if trailer_url:  # Check if trailer URL exists
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link
                    st.markdown("---")  # Display horizontal divider
            
            # Series by favorite person
            if content_type in ["Series", "Both"]:  # Check if user wants series recommendations
                st.subheader(f"Series featuring **{prefs['favorite_person']}**:")  # Display section header with person's name
                # Fetch series featuring this person
                person_series = get_series_by_actor(
                    prefs["favorite_person"],  # Person's name
                    episode_runtime_min=episode_runtime_min,  # Minimum episode runtime
                    episode_runtime_max=episode_runtime_max,  # Maximum episode runtime
                    year_min=year_min,  # Earliest air date
                    year_max=year_max,  # Latest air date
                    num_results=10  # Number of results to fetch
                )

                # Re-ranking using Machine Learning based on likes
                if liked_movies_list and person_series:  # Check if personalization data and results exist
                    person_series = reorder_movies_by_preference(person_series, liked_movies_list)  # Apply ML-based reordering
                
                # Loop through each series in the results
                for series in person_series:  # Iterate through series list
                    title = series.get("name")  # Get series name (note: "name" not "title" for TV)
                    overview = series.get("overview", "No description available.")  # Get overview (with default)
                    poster_path = series.get("poster_path")  # Get poster image path
                    poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None  # Build full poster URL if path exists
                    imdb_score = series.get("vote_average")  # Get IMDb rating
                    series_id = series.get("id")  # Get TMDB series ID
                    first_air_year = series.get("first_air_date", "")[:4]  # Extract year from first air date (first 4 characters)
                    trailer_url = get_trailer(series_id, "tv")  # Fetch trailer URL (note: content_type="tv")
                    series_genres = series.get("genre_ids", [])  # Get list of genre IDs for this series

                    # Create header row with Like/Dislike buttons
                    col1, col2 = st.columns([3, 1])  # Create two columns (3:1 ratio)
                    with col1:  # Left column for title
                        st.markdown(f"**{title}** ({first_air_year})")  # Display bold title with year
                    with col2:  # Right column for buttons
                        like_key = f"like_person_series_{series_id}"  # Create unique key for Like button
                        dislike_key = f"dislike_person_series_{series_id}"  # Create unique key for Dislike button
                
                        col_like, col_dislike = st.columns(2)  # Create two sub-columns for buttons
                        with col_like:  # Like button column
                            if st.button("Like", key=like_key):  # Create Like button
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=True)  # Save as liked series
                                st.success(f"Saved '{title}' to your preferences!")  # Show success message
                                st.rerun()  # Refresh page to apply changes
                        with col_dislike:  # Dislike button column
                            if st.button("Dislike", key=dislike_key):  # Create Dislike button
                                save_liked_movie(series_id, title, series_genres, imdb_score, liked=False)  # Save as disliked series
                                st.info(f"Noted that you don't like '{title}'")  # Show info message
                                st.rerun()  # Refresh page to apply changes
                    
                    # Display series details
                    if poster_url:  # Check if poster URL exists
                        st.image(poster_url, width=150)  # Display poster image
                    st.markdown(f"IMDb Score: {imdb_score}")  # Display rating
                    st.caption(overview)  # Display series overview
                    if trailer_url:  # Check if trailer URL exists
                        st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link
                    st.markdown("---")  # Display horizontal divider
        
        # Add spacing before Start Over button
        st.write("")  # Empty line for spacing
        if st.button("Start Over"):  # Create button to restart
            goto("step1")  # Navigate back to step 1
            st.rerun()

# ------------------- RANDOM MOVIE MODE -------------------
# Random Movie page: displays a random popular movie with details
elif st.session_state.page == "random":  # Check if current page is random
    st.title("Random Movie Generator")  # Display page title

    # Add spacing and back button
    st.write("")  # Empty line for spacing
    if st.button("← Back to Start"):  # Create back button with arrow
        goto("step1")  # Navigate back to step 1
        st.rerun()
    
    # Button to get a new random movie
    if st.button("Give me another random movie!"):  # Create refresh button
        st.rerun()  # Refresh page to get new random movie
    
    # Fetch and display random movie
    random_movie = get_random_movie()  # Get random movie from TMDB
    if random_movie:  # Check if movie was successfully fetched
        title = random_movie.get("title")  # Get movie title
        rating = random_movie.get("vote_average")  # Get IMDb rating
        overview = random_movie.get("overview", "No description available.")  # Get overview (with default)
        poster_path = random_movie.get("poster_path")  # Get poster image path
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None  # Build full poster URL (larger size: w500)
        movie_id = random_movie.get("id")  # Get TMDB movie ID
        release_year = random_movie.get("release_date", "")[:4]  # Extract year from release date (first 4 characters)
        trailer_url = get_trailer(movie_id, "movie")  # Fetch trailer URL

        # Display movie details
        st.markdown(f"## {title} ({release_year})")  # Display title as h2 header with year
        if poster_url:  # Check if poster URL exists
            st.image(poster_url, width=300)  # Display larger poster image
        st.markdown(f"### IMDb Score: {rating}")  # Display rating as h3 header
        st.markdown(f"Overview: {overview}")  # Display overview text
        if trailer_url:  # Check if trailer URL exists
            st.markdown(f"### [Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link as h3 header
    else:  # Movie fetch failed
        st.warning("Could not fetch a random movie. Try again!")  # Show warning message

# ------------------- RYAN GOSLING MODE -------------------
# Ryan Gosling page: displays top-rated Ryan Gosling movies
elif st.session_state.page == "gosling":  # Check if current page is gosling
    st.title("Ryan Gosling Recommendations")  # Display page title
    gosling_movies = get_ryan_gosling_movies()  # Fetch Ryan Gosling's top movies
    if gosling_movies:  # Check if movies were successfully fetched
        st.markdown("Sorted by IMDb Score (Highest First)")  # Display sorting information
        # Loop through each movie in the results
        for movie in gosling_movies:  # Iterate through movie list
            title = movie.get("title")  # Get movie title
            rating = movie.get("vote_average")  # Get IMDb rating
            overview = movie.get("overview", "No description available.")  # Get overview (with default)
            poster_path = movie.get("poster_path")  # Get poster image path
            poster_url = f"https://image.tmdb.org/t/p/w200{poster_path}" if poster_path else None  # Build full poster URL if path exists
            movie_id = movie.get("id")  # Get TMDB movie ID
            release_year = movie.get("release_date", "")[:4]  # Extract year from release date (first 4 characters)
            trailer_url = get_trailer(movie_id, "movie")  # Fetch trailer URL

            # Display movie details
            st.markdown(f"**{title}** ({release_year})")  # Display bold title with year
            if poster_url:  # Check if poster URL exists
                st.image(poster_url, width=150)  # Display poster image
            st.markdown(f"IMDb Score: {rating}")  # Display rating
            st.caption(overview)  # Display movie overview
            if trailer_url:  # Check if trailer URL exists
                st.markdown(f"[Watch Trailer]({trailer_url})", unsafe_allow_html=True)  # Display trailer link
            st.markdown("---")  # Display horizontal divider
    else:  # No movies found
        st.warning("No Ryan Gosling movies found.")  # Show warning message

    # Add spacing and back button
    st.write("")  # Empty line for spacing
    if st.button("← Back to Start"):  # Create back button with arrow
        goto("step1")  # Navigate back to step 1
        st.rerun()
