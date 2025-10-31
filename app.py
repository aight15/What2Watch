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
    We are happy to help you choose your movie/serie night by suggesting THE BEST movie or serie, tailored to your needs.
    
    
    
    *Our app combines real-time data, past movie/serie choices paired with machine learning, to give you personalized movie/serie suggestions that match your style.*
    ---
    """)
