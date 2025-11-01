import streamlit as st

# here we start with the formatting of the Welcome Page
st.set_page_config(page_title="What2Watch", page_icon="logo.jpg")

# The following parts represent the formatting of the layout for the user (logo, inputs: name, budget type, current location) 
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=700) 
if "page" not in st.session_state:
    st.session_state.page = "user_info"
# this is the navigation function
def goto(page_name):
    st.session_state.page = page_name
if st.session_state.page == "user_info":
    st.title("Welcome to What2Watch")
    st.write("_Define your preferred criteria and find the perfect Movie or Series!_")
# Introduction to our app and explanation of our business case (on a sidebar)
    st.sidebar.markdown(""" 
    Findin a movie or a series can be complicated and time-consuming. 
    With countless Movies/Series, genres, lengths and personal preferences, finding the PERFECT movie/serie is often stressful and time-consuming.
    
    ---
    
    How What2Watch helps you?
    We are happy to help you choose your movie/series night by suggesting THE BEST movie or series, tailored to your needs.
    
    
    
    *Our app combines real-time data, past movie/series choices paired with machine learning, to give you personalised movie/series suggestions that match your style.*
    ---
    """)

# start of questions
import requests

# TMDb API Key
TMDB_API_KEY = "ef26791dfc9c3b8254044fe9167e3edb"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

GENRE_MAP = {
    "Action": 28, "Comedy": 35, "Drama": 18, "Romance": 10749,
    "Horror": 27, "Sci-Fi": 878, "Documentary": 99,
    "Animation": 16, "Mystery": 9648, "Thriller": 53
}

MOOD_GENRE_SUGGESTION = {
    "Happy": ["Comedy", "Animation"],
    "Sad": ["Romance", "Documentary"],
    "Adventurous": ["Action", "Sci-Fi"],
    "Romantic": ["Romance", "Drama"],
    "Bored": ["Thriller", "Mystery"],
    "Scared": ["Horror"],
    "Thoughtful": ["Drama", "Documentary"]
}

def get_movies_by_genre(genre_id):
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "en-US"
 }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])[:5]
    return []

if "preferences" not in st.session_state:
    st.session_state.preferences = {}

with st.form("movie_form"):

    mood = st.selectbox("How are you feeling today?", list(MOOD_GENRE_SUGGESTION.keys()))

    genre_choice = st.multiselect(
        "Which genre are you interested in?",
        options=list(GENRE_MAP.keys()),
        default=MOOD_GENRE_SUGGESTION.get(mood, [])
    )

    streaming_services = st.multiselect(
        "Which streaming services do you have?",
        ["Netflix", "Amazon Prime", "Disney+", "HBO Max", "Hulu", "Apple TV+", "Other"]
    )

    content_type = st.radio("Film or Series or both?", ["Film", "Series", "Both"])

    time_available = st.radio(
        "How much time do you have?",
        ["< 1 hour", "1–2 hours", "2–3 hours", "3+ hours"]
    )

    realism = st.radio("Should the movie be realistic or a fantasy?", ["Realistic", "Fantasy"])

    modern_or_classic = st.radio("Modern or classic?", ["Modern", "Classic", "Doesn't matter"])

    watching_group = st.radio("Are you watching alone or in a group?", ["Alone", "In a group"])

    gosling_fan = st.radio("Do you like Ryan Gosling?", ["Yes", "No", "Not sure"])

    length = st.radio("Preferred movie length:", ["Short (< 90 min)", "Medium (90–120 min)", "Long (> 120 min)"])
    intensity = st.slider("How intense should the movie be?", 1, 10, 5)
    fav_movie = st.text_input("What's a movie you've liked recently?")

    submitted = st.form_submit_button("🎥 Recommend Me Something!")

if submitted:
    # Store user preferences
    st.session_state.preferences = {
        "mood": mood,
        "genres": genre_choice,
        "streaming_services": streaming_services,
        "content_type": content_type,
        "time_available": time_available,
        "realism": realism,
        "modern_or_classic": modern_or_classic,
        "watching_group": watching_group,
        "gosling_fan": gosling_fan,
        "length": length,
        "intensity": intensity,
        "favorite_movie": fav_movie
    }

    
