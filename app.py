import pickle
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #FF6B35;
    --secondary: #F7931E;
    --dark-bg: #0F1419;
    --card-bg: #1A1F2E;
    --border-color: #2A3142;
    --text-primary: #FFFFFF;
    --text-secondary: #B0B8C1;
    --accent: #00D9FF;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--dark-bg) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { 
    padding: 2rem 2rem !important; 
    max-width: 1600px !important;
}

/* Header */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
}

.header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-credit {
    text-align: right;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.header-credit-name {
    color: var(--secondary);
    font-weight: 600;
    margin-top: 0.25rem;
}

/* Search Section */
label {
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.5rem !important;
}

.search-section {
    margin-bottom: 2rem;
    display: flex;
    gap: 1rem;
    align-items: flex-end;
}

.stSelectbox > div > div {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 0.75rem !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
}

.stSelectbox > div > div:hover {
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(255, 107, 53, 0.1) !important;
}

/* Fix selectbox text visibility */
.stSelectbox > div > div > div {
    color: var(--text-primary) !important;
}

.stSelectbox input {
    color: var(--text-primary) !important;
}

.stSelectbox [data-baseweb="select"] > div {
    color: var(--text-primary) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%) !important;
    color: white !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.2) !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3) !important;
}

/* Images */
.stImage img {
    border-radius: 12px !important;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
}

.stImage img:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 50px rgba(255, 107, 53, 0.3) !important;
}

/* Section Headers */
.section-header {
    font-family: 'Poppins', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-header::before {
    content: '';
    width: 4px;
    height: 24px;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    border-radius: 2px;
}

/* Selected Movie Section */
.selected-movie-container {
    background: linear-gradient(135deg, var(--card-bg) 0%, rgba(26, 31, 46, 0.5) 100%);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 3rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.movie-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1.2rem;
    line-height: 1.3;
}

.movie-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.05rem;
    color: var(--text-primary);
}

.meta-label {
    color: var(--secondary);
    font-weight: 700;
}

/* Rating Badge */
.rating-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 107, 53, 0.15);
    border: 2px solid var(--primary);
    border-radius: 25px;
    padding: 0.6rem 1.2rem;
    font-size: 1.05rem;
    color: var(--primary);
    font-weight: 700;
    margin-bottom: 1.2rem;
}

/* Genre Badges */
.genre-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem;
    margin-bottom: 1.8rem;
}

.genre-badge {
    background: rgba(255, 107, 53, 0.08);
    border: 1px solid rgba(255, 107, 53, 0.3);
    border-radius: 20px;
    padding: 0.5rem 1rem;
    font-size: 0.95rem;
    color: var(--text-primary);
    font-weight: 500;
    transition: all 0.3s ease;
}

.genre-badge:hover {
    background: rgba(255, 107, 53, 0.15);
    border-color: var(--primary);
    color: var(--primary);
    transform: translateY(-2px);
}

/* Synopsis */
.synopsis {
    font-size: 1.05rem;
    line-height: 1.9;
    color: #E0E0E0;
    padding: 1.2rem;
    background: rgba(0, 0, 0, 0.3);
    border-left: 4px solid var(--primary);
    border-radius: 8px;
    margin-top: 0.5rem;
}

/* Recommendations Grid */
.recommendations-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.rec-card {
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
}

.rec-card:hover {
    border-color: var(--primary);
    box-shadow: 0 12px 40px rgba(255, 107, 53, 0.15);
    transform: translateY(-4px);
}

.rec-card-number {
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.75rem;
    text-align: center;
    background: rgba(247, 147, 30, 0.05);
    border-bottom: 1px solid var(--border-color);
}

.rec-card-title {
    font-family: 'Poppins', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    padding: 0.85rem;
    text-align: center;
    border-top: 2px solid var(--primary);
    min-height: 55px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1.3;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    padding: 0.75rem !important;
}

.streamlit-expanderHeader:hover {
    background: rgba(255, 107, 53, 0.08) !important;
    border-color: var(--primary) !important;
}

.streamlit-expanderContent {
    background: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid var(--border-color) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 1.2rem !important;
}

/* Footer */
.footer {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
    color: var(--text-secondary);
    font-size: 0.85rem;
}

hr { border-color: var(--border-color) !important; }

.stSpinner > div { border-top-color: var(--primary) !important; }
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--primary), var(--secondary)) !important;
}

/* Responsive */
@media (max-width: 1200px) {
    .recommendations-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    .block-container {
        max-width: 100% !important;
        padding: 1.5rem 1rem !important;
    }
}

@media (max-width: 768px) {
    .recommendations-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    .header-title {
        font-size: 1.8rem;
    }
    .movie-title {
        font-size: 1.5rem;
    }
    .section-header {
        font-size: 1.1rem;
    }
    .block-container {
        padding: 1rem 0.75rem !important;
    }
    .stButton > button {
        padding: 0.6rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
}

@media (max-width: 480px) {
    .recommendations-grid {
        grid-template-columns: 1fr;
    }
    .header-title {
        font-size: 1.5rem;
        letter-spacing: 2px;
    }
    .movie-title {
        font-size: 1.3rem;
    }
    .section-header {
        font-size: 1rem;
    }
    .rating-badge {
        font-size: 0.85rem;
        padding: 0.4rem 0.8rem;
    }
    .genre-badge {
        font-size: 0.8rem;
        padding: 0.35rem 0.75rem;
    }
    .synopsis {
        font-size: 0.9rem;
        padding: 0.9rem;
    }
    .meta-item {
        font-size: 0.9rem;
    }
}
</style>
""", unsafe_allow_html=True)

# Load data
movies = pickle.load(open('models/movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

API_KEY = "7b8b7f8b9e3e9d3b0ab494f8f184edee"


def fetch_movie_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
    except Exception:
        return {
            "poster": "https://via.placeholder.com/500x750?text=No+Image",
            "title": "Unknown",
            "overview": "Unavailable.",
            "rating": "N/A",
            "vote_count": 0,
            "release_date": "N/A",
            "genres": "N/A",
            "runtime": "N/A",
            "year": "N/A",
        }

    poster_path = data.get('poster_path')
    poster = ("https://image.tmdb.org/t/p/w500/" + poster_path) if poster_path else "https://via.placeholder.com/500x750?text=No+Image"

    genres = ", ".join([g['name'] for g in data.get('genres', [])]) or "N/A"
    runtime = data.get('runtime')
    runtime_str = f"{runtime // 60}h {runtime % 60}m" if runtime else "N/A"
    release = data.get('release_date', 'N/A')
    year = release[:4] if release and release != 'N/A' else 'N/A'

    return {
        "poster": poster,
        "title": data.get('title', 'N/A'),
        "overview": data.get('overview', 'No description available.'),
        "rating": data.get('vote_average', 'N/A'),
        "vote_count": data.get('vote_count', 0),
        "release_date": release,
        "year": year,
        "genres": genres,
        "runtime": runtime_str,
    }


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    recommended = []
    progress_bar = st.progress(0)
    for i, val in enumerate(distances[1:6]):
        movie_id = movies.iloc[val[0]].movie_id
        recommended.append(fetch_movie_details(movie_id))
        progress_bar.progress((i + 1) / 5)
    progress_bar.empty()
    return recommended


# ── Header ─────────────────────────────────────────────────────────────────────
col_title, col_credit = st.columns([3, 1])
with col_title:
    st.markdown('<div class="header-title">🎬 MOVIE RECOMMENDER</div>', unsafe_allow_html=True)
with col_credit:
    st.markdown(
        '<div class="header-credit" style="display: none;">BY<div class="header-credit-name">NAVNEET MALLICK</div></div>'
        '<style>@media (min-width: 768px) { .header-credit { display: block !important; } }</style>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Search Section ─────────────────────────────────────────────────────────────
movie_list = movies['title'].values
selected_movie = st.selectbox("🔎 Select a movie to get recommendations", movie_list)

col_btn, col_space = st.columns([1, 4])
with col_btn:
    recommend_btn = st.button("🎯 Get Recommendations", use_container_width=True)

if recommend_btn:
    with st.spinner("Finding perfect matches... 🎥"):
        recommended_movies = recommend(selected_movie)

    # Fetch selected movie details
    sel_index = movies[movies['title'] == selected_movie].index[0]
    sel_id = movies.iloc[sel_index].movie_id
    selected_details = fetch_movie_details(sel_id)

    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)

    # ── Selected Movie (Compact Banner) ────────────────────────────────────────
    st.markdown(
        '<div style="background: linear-gradient(135deg, rgba(255, 107, 53, 0.08) 0%, rgba(247, 147, 30, 0.05) 100%); '
        'border: 1px solid rgba(255, 107, 53, 0.2); border-left: 4px solid var(--primary); '
        'border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 2rem;">'
        f'<div style="display: flex; align-items: center; gap: 1rem;">'
        f'<div style="font-size: 1.1rem; color: var(--text-secondary);">Because you selected:</div>'
        f'<div style="font-family: Poppins, sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--primary);">{selected_details["title"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # ── Recommendations Section (Main Focus) ───────────────────────────────────
    st.markdown('<div class="section-header">🎯 Recommended For You</div>', unsafe_allow_html=True)

    rec_cols = st.columns(5, gap="large")

    for i, rec in enumerate(recommended_movies):
        with rec_cols[i]:
            st.markdown(f'<div class="rec-card-number">#{i+1}</div>', unsafe_allow_html=True)
            st.image(rec['poster'], use_container_width=True)
            st.markdown(f'<div class="rec-card-title">{rec["title"]}</div>', unsafe_allow_html=True)

            with st.expander("📋 Details"):
                if isinstance(rec['rating'], (int, float)):
                    st.markdown(
                        f'<div class="rating-badge">★ {rec["rating"]}/10 · {rec["vote_count"]:,} votes</div>',
                        unsafe_allow_html=True,
                    )
                if rec['genres'] != 'N/A':
                    genres_html = ''.join(
                        f'<div class="genre-badge">{g.strip()}</div>'
                        for g in rec['genres'].split(',')
                    )
                    st.markdown(f'<div class="genre-container">{genres_html}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="movie-meta">'
                    f'<div class="meta-item"><span class="meta-label">Year:</span> {rec["year"]}</div>'
                    f'<div class="meta-item"><span class="meta-label">Runtime:</span> {rec["runtime"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f'<div class="synopsis">{rec["overview"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)

    # ── Selected Movie Full Details (Expandable) ───────────────────────────────
    with st.expander("📽️ View Full Details of Your Selection", expanded=False):
        col_poster, col_info = st.columns([1.2, 2.5], gap="large")

        with col_poster:
            st.image(selected_details['poster'], use_container_width=True)

        with col_info:
            st.markdown(f'<div class="movie-title">{selected_details["title"]}</div>', unsafe_allow_html=True)

            # Rating
            if isinstance(selected_details['rating'], (int, float)):
                st.markdown(
                    f'<div class="rating-badge">★ {selected_details["rating"]}/10 · {selected_details["vote_count"]:,} votes</div>',
                    unsafe_allow_html=True,
                )

            # Meta info
            st.markdown(
                f'<div class="movie-meta">'
                f'<div class="meta-item"><span class="meta-label">Year:</span> {selected_details["year"]}</div>'
                f'<div class="meta-item"><span class="meta-label">Runtime:</span> {selected_details["runtime"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Genres
            if selected_details['genres'] != 'N/A':
                genres_html = ''.join(
                    f'<div class="genre-badge">{g.strip()}</div>'
                    for g in selected_details['genres'].split(',')
                )
                st.markdown(f'<div class="genre-container">{genres_html}</div>', unsafe_allow_html=True)

            # Synopsis
            st.markdown('<div style="margin-top: 1rem; margin-bottom: 0.5rem;"><span class="meta-label" style="font-size: 1.1rem;">Synopsis:</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="synopsis">{selected_details["overview"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="footer">Made with ❤️ by Navneet Mallick</div>', unsafe_allow_html=True)
