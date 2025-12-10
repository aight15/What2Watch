# What2Watch — Movie & Series Finder

## Overview

- Goals and Objectives
- Features
  - Data sources and API's
  - [Personalization (“ML‑Light”)](#personalization-mllight)
  - [Core Functions](#core-functions)
  - [User Flow](#user-flow)
- [Architecture & Tech Stack](#architecture--tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run](#run)
- [Data & Persistence](#data--persistence)
- [UX Details](#ux-details)
- [Limitations](#limitations)
- [Roadmap](#roadmap)
- [Disclosures & Credits](#disclosures--credits)

---

## Goals

A Streamlit app that recommends movies and TV series from TMDB based on simple preferences and a personalization layer. Users pick formats, runtime, animation vs. live-action, modern vs. classic, genres, and optionally a favorite actor/director. Results include posters, brief overviews, IMDb-style scores, and trailer links. Likes are saved locally and used to re-rank future results. fileciteturn1file1

- Help users find a **watchlist quickly** without endless scrolling.
- Provide **intuitive controls**: genres, runtime, animation, modern/classic, popularity.
- Deliver **light personalization** using saved likes + cosine similarity. fileciteturn1file2

---

## Features

### Data Sources & APIs
- **TMDB (The Movie Database)** for discovery endpoints (movie/TV), person search, and videos (YouTube keys):
  - `/discover/movie`, `/discover/tv`, `/search/person`, `/{type}/{id}/videos`.
  - Sorting by `popularity.desc` or `vote_average.desc` with sensible `vote_count` floors. fileciteturn1file4
- **Images** via TMDB posters (`image.tmdb.org/t/p/w200|w500`). fileciteturn1file16

### Personalization (“ML‑Light”)
- Build **feature vectors** per title: one‑hot **genre_ids** + normalized **vote_average** + log‑scaled **popularity**.
- Aggregate **user profile** from liked titles; re-rank candidates by **cosine_similarity**. fileciteturn1file7
- Preferences persist in a local JSON file `liked_movies.json`. fileciteturn1file6

### Core Functions
- `get_movies_by_genre(...)` / `get_series_by_genre(...)`: Discover with filters (animation, runtime/years). TV runtime filters are intentionally limited (API constraints). fileciteturn1file4
- `get_movies_by_actor_or_director(...)` / `get_series_by_actor(...)`: Person search → discover by `with_cast`. fileciteturn1file11
- `get_ryan_gosling_movies()`: Fun page fetching Gosling’s top‑rated films. fileciteturn1file6
- `get_random_movie()`: Truly random popular film (random page + random pick). fileciteturn1file10
- `get_trailer(...)`: YouTube trailer via TMDB videos. fileciteturn1file10
- `load_liked_movies()` / `save_liked_movie(...)`: Read/write simple local preferences. fileciteturn1file6

### User Flow
1. **Step 1**: Choose **Film**, **Series**, or **Both**. fileciteturn1file9  
2. **Step 2**: Set runtime, animation vs. live‑action, modern vs. classic, genre(s), popularity, and an optional favorite actor/director. Sidebar quiz helps infer preferred genres and draws a radar chart. fileciteturn1file3
3. **Results**: Per‑genre sections with poster, score, overview, **trailer link**, and **Like/Dislike**. Lists are optionally re‑ranked by your likes. fileciteturn1file18
4. **Special Modes**: **Random Movie** and **Ryan Gosling** pages. fileciteturn1file16

---

## Architecture & Tech Stack

- **Frontend/Host**: Streamlit, multi‑page navigation via `st.session_state`. fileciteturn1file1
- **Core Libraries**: `requests` (TMDB), `numpy`, `scikit-learn` (`cosine_similarity`), `matplotlib` (radar chart). fileciteturn1file1
- **Local Storage**: `liked_movies.json` in project root. fileciteturn1file6

---

## Installation

**Prerequisites**
- Python **3.10+**
- `pip` and a virtual environment

**Setup**
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install streamlit numpy requests scikit-learn matplotlib
```

Optional: create `requirements.txt` for reproducible installs.

---

## Configuration

**TMDB API Key**: recommended via environment variable (avoid hardcoding in production).

```bash
# macOS/Linux
export TMDB_API_KEY="YOUR_KEY"
# PowerShell
$env:TMDB_API_KEY="YOUR_KEY"
```

Update code to read `os.getenv("TMDB_API_KEY")`. The current script includes a hardcoded key placeholder — **do not ship** secrets this way. fileciteturn1file3

**Streamlit config (optional)**: place images like `logo.jpg` in project root; app uses `st.set_page_config(...)`. fileciteturn1file1

---

## Run

```bash
streamlit run Projekt_1.11.25_fixed.py
```

- App opens in your default browser.  
- Navigate via **Next/Back**, **Random Movie**, **Ryan Gosling**.  
- Pick genres, runtime, etc., and browse recommendations with trailers. fileciteturn1file9

---

## Data & Persistence

- Likes/Dislikes are stored in `liked_movies.json` as simple dict entries (id, title, genres, rating, liked). fileciteturn1file7
- No external user accounts; delete or edit the file to reset preferences.

---

## UX Details

- **Sidebar quiz**: Quick checkboxes for known titles; computes a per‑genre score and draws a polar **radar chart** for guidance. fileciteturn1file3
- **Results lists**: Each genre renders a compact card with poster, score, overview, trailer link, and Like/Dislike buttons. Re‑ranking applies when likes exist. fileciteturn1file18
- **Stateful pages**: Navigation managed in `st.session_state.page`. fileciteturn1file1

---

## Limitations

- **Data quality**: `vote_average` can be noisy; the “underrated” path lowers `vote_count` thresholds and may surface outliers. fileciteturn1file4
- **TV runtimes**: TMDB episode runtime metadata is inconsistent; filtering is limited by the API. fileciteturn1file4
- **Simple model**: The re‑ranker uses only genres, rating, and popularity — a pragmatic **hinting system**, not a full recommender. fileciteturn1file7
- **Local persistence**: JSON file is single‑user and unsynced; no multi‑device support. fileciteturn1file7


## Disclosures & Credits

- 
