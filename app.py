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

    
