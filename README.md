# What2Watch — Movie & Series Finder

## Overview

- Goals and Objectives
- Features
  - Data sources and API's
  - Machine Learning
  - Core Functions
  - User experience
  - Database Design
- Limitations
- Disclosure
- Team Structure

---

## Goals and Objectives

A Streamlit app that recommends movies and TV series from TMDB based on simple preferences and a personalization layer. 
Users pick formats, runtime, animation vs. live-action, modern vs. classic, genres, and optionally a favorite actor/director. 
Results include:
- Posters of the Recommendation
- Brief overviews
- IMDb-style scores
- Trailer links
Likes are saved locally and used to re-rank future results. 

---

## Features

### Data Sources & APIs
- **TMDB (The Movie Database)** for discovery endpoints (movie/TV), person search, and videos (YouTube keys):
- **Images** via TMDB posters 

---

### Machine Learing
Each Recommendation based on the specified preferences has a like and dislike button next to it.
The likes and Dislikes will re-rank the future results, so it won't just be deleted out of the Recommendations. The likes will appear on top of Future lists and the dislikes at the bottom

---

### Core Functions
- `get_movies_by_genre(...)` / `get_series_by_genre(...)`: Discover with filters (animation, runtime/years). TV runtime filters are intentionally limited (API constraints). fileciteturn1file4
- `get_movies_by_actor_or_director(...)` / `get_series_by_actor(...)`: Person search → discover by `with_cast`. fileciteturn1file11
- `get_ryan_gosling_movies()`: Fun page fetching Gosling’s top‑rated films. fileciteturn1file6
- `get_random_movie()`: Truly random popular film (random page + random pick). fileciteturn1file10
- `get_trailer(...)`: YouTube trailer via TMDB videos. fileciteturn1file10
- `load_liked_movies()` / `save_liked_movie(...)`: Read/write simple local preferences. fileciteturn1file6

### User experience
1. **Step 1**:
   Choose **Film**, **Series**, or **Both**.

   Or there are also Options like:
   **Random Movie**
   As the name says, it will give you a random movie

   **Ryan Gosling Button**
   It will recommend the highest rated Ryan gosling Movies, because who doesn't
   like Ryan Gosling ;)
   
3. **Step 2**:
  Set runtime, animation vs. live‑action, modern vs. classic, genre(s), popularity, and an optional favorite actor/director. Sidebar quiz helps infer preferred genres and draws a radar chart.

4. **Result Page**:
Per‑genre sections with poster, score, overview of the movie, trailer link, and **Like/Dislike Button** for future Recommendations.
You can also navigate with **Back** and **Next** to change certain preferences and to check the Questions again

Details:
- **Sidebar quiz**: Quick checkboxes for known titles; computes a per‑genre score and draws a polar **radar chart** for guidance. fileciteturn1file3
- **Results lists**: Each genre renders a compact card with poster, score, overview, trailer link, and Like/Dislike buttons. Re‑ranking applies when likes exist.
- **Stateful pages**: Navigation managed in `st.session_state.page`.
  
---

## Database design
- Likes/Dislikes are stored in `liked_movies.json` as simple dict entries (id, title, genres, rating, liked). fileciteturn1file7
- No external user accounts; delete or edit the file to reset preferences.

---

## Limitations

- **Profile**: Although the Web Application gives us recommendations based on our preferences there is no Profile, which could also be helpful to keep a track of movies weve already seen. also a Final Ranking would enable us to save our favorite Movies in our Profile.
  
- **TV runtimes**: TMDB episode runtime metadata is inconsistent; filtering is limited by the API.
  
- **Simple model**: The re‑ranker uses only genres, rating, and popularity — a pragmatic **hinting system** so it wont 100% fulfil the mood in which the user is. With the Categories it tries to find out the Preference but it could also be wrong.

- **quantity of Categories**: There are also alot of Categories which play a role in finding the right movie for the night. These Categories also play a role for the Recommendation but we had to limit ourselves to the central categories.
  
- **Local persistence**: JSON file is single‑user and unsynced; no multi‑device support.

---

## Disclosures & Credits

- ChatGPT was used to generate the general structure, to add to the ideas we had. it helped us to bring our Ideas into a line of Code, from where we could continue to build our Webpage

- ChatGPT helped us to add knowledge about specific functions, so we could use the knowledge to implement it to our Code

- Excluding the general structure, AI was only used for high-level guidance advice, suggestions for structuring Code so the overview of the Code was clear and structure.
It was also used for Implementation tips. So anytime ChatGPT was used we noted that part in our source comments with a tag

- Familiy and Friends of the Group added their knowledge with tips and tricks to improve our Web applications for unanswered Questions about functionality.

---

## Team Structure
This Matrix shows the structure and Organization inside our Team, it visualizes roles, responsibilities and documents individual Contributions to the Project in a contribution Matrix.

