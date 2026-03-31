import pickle
import streamlit as st
import requests
import time

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap');

:root {
    --gold: #F5C518;
    --accent: #e05c2a;
    --dark: #0a0a0a;
    --card: #141414;
    --border: #252525;
    --text: #f0f0f0;
    --muted: #777;
    --radius: 12px;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--dark) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem !important; max-width: 1300px; }

h1 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 3rem !important;
    letter-spacing: 4px !important;
    background: linear-gradient(90deg, #F5C518, #e05c2a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.stSelectbox > div > div {
    background: #1c1c1c !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
label { color: var(--muted) !important; font-size: 0.8rem !important; letter-spacing: 1px; text-transform: uppercase; }

.stButton > button {
    background: linear-gradient(90deg, var(--gold), var(--accent)) !important;
    color: #000 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 2.5rem !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stImage img {
    border-radius: var(--radius) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.stImage img:hover {
    transform: translateY(-5px);
    box-shadow: 0 16px 40px rgba(245, 197, 24, 0.2);
}

div[style*="background-color: #f0f2f6"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--gold) !important;
    border-radius: 0 0 10px 10px !important;
}
div[style*="background-color: #f0f2f6"] p {
    color: var(--text) !important;
    font-size: 0.82rem !important;
}

div[style*="background-color: #e8f4f8"] {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--gold) !important;
    border-radius: 8px !important;
}
div[style*="background-color: #e8f4f8"] p {
    color: var(--text) !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: #1a1a1a !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
}
.streamlit-expanderContent {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 10px !important;
}

/* Detail badges inside expander */
.detail-badge {
    display: inline-block;
    background: #222;
    border: 1px solid #333;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    color: #bbb;
    margin: 2px 2px 4px 0;
}
.rating-badge {
    display: inline-block;
    background: rgba(245, 197, 24, 0.12);
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    color: var(--gold);
    font-weight: 600;
    margin-bottom: 6px;
}
.overview-text {
    font-size: 0.78rem;
    color: #999;
    line-height: 1.55;
    border-top: 1px solid #222;
    padding-top: 8px;
    margin-top: 6px;
}

hr { border-color: #222 !important; }
h5 {
    color: var(--muted) !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border-left: 3px solid var(--gold);
    padding-left: 10px;
}
.stSpinner > div { border-top-color: var(--gold) !important; }
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--gold), var(--accent)) !important;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender System")
st.write("")

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
            "title": "Unknown", "overview": "Unavailable.", "rating": "N/A",
            "vote_count": 0, "release_date": "N/A", "genres": "N/A", "runtime": "N/A",
        }

    poster_path = data.get('poster_path')
    poster = ("https://image.tmdb.org/t/p/w500/" + poster_path) if poster_path \
        else "https://via.placeholder.com/500x750?text=No+Image"

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
    recommended_movies = []
    progress_bar = st.progress(0)
    for i, val in enumerate(distances[1:6]):
        movie_id = movies.iloc[val[0]].movie_id
        recommended_movies.append(fetch_movie_details(movie_id))
        progress_bar.progress((i + 1) / 5)
    progress_bar.empty()
    return recommended_movies

movie_list = movies['title'].values
selected_movie = st.selectbox("🔎 Search or select a movie", movie_list)

if st.button("Recommend Movies"):
    with st.spinner("Finding similar movies... 🎥"):
        recommended_movies = recommend(selected_movie)

    # Get selected movie details
    selected_index = movies[movies['title'] == selected_movie].index[0]
    selected_movie_id = movies.iloc[selected_index].movie_id
    selected_details = fetch_movie_details(selected_movie_id)

    # ── Header banner ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0;'>✨ Recommended Movies Based On</h2>
        <h3 style='color: #FFD700; margin: 10px 0 0 0;'>{selected_movie}</h3>
    </div>
    """, unsafe_allow_html=True)

    # ── Top 5 Recommendations ──────────────────────────────────────────────────
    st.markdown("##### Top 5 Recommendations:")
    cols = st.columns(5, gap="medium")

    for i, rec in enumerate(recommended_movies):
        with cols[i]:
            # Poster
            st.image(rec['poster'], use_container_width=True)   # ✅ Fixed

            # Movie title card
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; background-color: #f0f2f6;
                        border-radius: 8px; margin-top: 10px;'>
                <p style='font-weight: bold; font-size: 13px; margin: 0; color: #000;'>{rec['title']}</p>
            </div>
            """, unsafe_allow_html=True)

            # Expander with details
            with st.expander("ℹ️ Details"):
                # Rating
                if isinstance(rec['rating'], (int, float)):
                    st.markdown(f"""
                    <div class='rating-badge'>★ {rec['rating']}/10
                    &nbsp;·&nbsp; {rec['vote_count']:,} votes</div>
                    """, unsafe_allow_html=True)

                # Genres as badges
                if rec['genres'] != 'N/A':
                    badges = "".join(
                        f"<span class='detail-badge'>{g.strip()}</span>"
                        for g in rec['genres'].split(',')
                    )
                    st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)

                # Year & Runtime
                st.markdown(f"""
                <div style='margin: 6px 0;'>
                    <span class='detail-badge'>📅 {rec['year']}</span>
                    <span class='detail-badge'>⏱ {rec['runtime']}</span>
                </div>
                """, unsafe_allow_html=True)

                # Overview
                st.markdown(f"""
                <div class='overview-text'>{rec['overview']}</div>
                """, unsafe_allow_html=True)

    # ── Selected movie at bottom ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("##### 🎬 Your Selection:")
    col_sel = st.columns([1, 2, 1])
    with col_sel[1]:
        st.image(selected_details['poster'], use_container_width=True)   # ✅ Fixed
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background-color: #e8f4f8;
                    border-radius: 8px; margin-top: 10px; border-left: 4px solid #667eea;'>
            <p style='font-weight: bold; font-size: 16px; margin: 0; color: #000;'>{selected_movie}</p>
        </div>
        """, unsafe_allow_html=True)

        # Expander for selected movie too
        with st.expander("ℹ️ Details"):
            if isinstance(selected_details['rating'], (int, float)):
                st.markdown(f"""
                <div class='rating-badge'>★ {selected_details['rating']}/10
                &nbsp;·&nbsp; {selected_details['vote_count']:,} votes</div>
                """, unsafe_allow_html=True)

            if selected_details['genres'] != 'N/A':
                badges = "".join(
                    f"<span class='detail-badge'>{g.strip()}</span>"
                    for g in selected_details['genres'].split(',')
                )
                st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div style='margin: 6px 0;'>
                <span class='detail-badge'>📅 {selected_details['year']}</span>
                <span class='detail-badge'>⏱ {selected_details['runtime']}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='overview-text'>{selected_details['overview']}</div>
            """, unsafe_allow_html=True)

            st.write("Developed with ❤️ By Navneet")
