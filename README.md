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

A common Problem among alot of People is indecisiveness when it comes to Movies. We all were at that point, where we searched for a movie to watch but couldn't find anything that matched your preferences perfectly. So main goal of What2Watch is to remove the obstacles standing between the user and a great movie.

What2watch recommends movies and TV series from TMDB based on simple preferences and a personalization layer. 
Users pick formats, runtime, animation vs. live-action, modern vs. classic, genres, and optionally a favorite actor/director. It also offers and random button and a Ryan Gosling button.
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
What2Watch uses a simple personalized recommendation system that learns from each user’s likes and dislikes. Every movie or series is converted into a numerical profile based on its genres, rating, and popularity. When the user likes an item, this profile is saved and combined with previous likes to form a user preference model. New recommendations are then compared to this model, and the most similar items are shown at the top. Disliked items are noted and moved further down in future lists. As the user interacts with the app, the system continually improves and becomes better at predicting what the user will enjoy.

---

### Core Functions
- `get_movies_by_genre(...)` / `get_series_by_genre(...)`: Discover with filters (animation, runtime/years). TV runtime filters are intentionally limited (API constraints). 
- `get_movies_by_actor_or_director(...)` / `get_series_by_actor(...)`: Person search → discover by `with_cast`. 
- `get_ryan_gosling_movies()`: Fun page fetching Gosling’s top‑rated films.
- `get_random_movie()`: Truly random popular film (random page + random pick). 
- `get_trailer(...)`: YouTube trailer via TMDB videos.
- `load_liked_movies()` / `save_liked_movie(...)`: Read/write simple local preferences.

### User experience
1. **Step 1**:
   Choose **Film**, **Series**, or **Both**.
   
3. **Step 2**:
  Set runtime, animation vs. live‑action, modern vs. classic, genre(s), popularity, and an optional favorite actor/director. Sidebar quiz helps infer preferred genres and draws a radar chart.

4. **Result Page**:
Per‑genre sections with poster, score, overview of the movie, trailer link, and **Like/Dislike Button** for future Recommendations.
You can also navigate with **Back** and **Next** to change certain preferences and to check the Questions again.

additional features:
- **Sidebar quiz**: Quick checkboxes for known titles; computes a per‑genre score and draws a polar **radar chart** for guidance.
- **Random Movie**: As the name says, it will give you a random movie
- **Ryan Gosling Button**: It will recommend the highest rated Ryan gosling Movies, because who doesn't
   like Ryan Gosling ;)

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

- ChatGPT was used to generate the general structure, to add to the ideas we had. it helped us to bring our Ideas into a line of Code, from where we could continue to build our Webpage.

- ChatGPT helped us to add knowledge about specific functions, so we could use the knowledge to implement it to our Code.

- Excluding the general structure, AI was only used for high-level guidance advice, suggestions for structuring Code so the overview of the Code was clear and structure.
It was also used for Implementation tips. So anytime ChatGPT was used we noted that part in our source comments with a tag.

- Familiy and Friends of the Group added their knowledge with tips and tricks to improve our Web applications for unanswered Questions about functionality.

---

## Team Structure
This Matrix shows the structure and Organization inside our Team, it visualizes roles, responsibilities and documents individual Contributions to the Project in a contribution Matrix.
<img width="1645" height="660" alt="image" src="https://github.com/user-attachments/assets/70677242-5d5a-47a1-940b-b7a5e9bc4d80" />


