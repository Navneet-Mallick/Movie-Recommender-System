import pickle
import streamlit as st
import requests

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
.block-container { padding-top: 2rem !important; max-width: 1400px; }

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

/* Movie card label */
.movie-label {
    text-align: center;
    padding: 8px 6px;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-top: 2px solid var(--gold);
    border-radius: 0 0 10px 10px;
    margin-top: 6px;
}
.movie-label p {
    font-weight: 600;
    font-size: 0.82rem;
    margin: 0;
    color: var(--text) !important;
    line-height: 1.3;
}

/* Section label above columns */
.col-section-label {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
    margin-bottom: 6px;
}
.col-section-label-selected {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--gold);
    text-align: center;
    margin-bottom: 6px;
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
            "year": "N/A",
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
    recommended = []
    progress_bar = st.progress(0)
    for i, val in enumerate(distances[1:6]):
        movie_id = movies.iloc[val[0]].movie_id
        recommended.append(fetch_movie_details(movie_id))
        progress_bar.progress((i + 1) / 5)
    progress_bar.empty()
    return recommended


def render_details(details):
    """Render the expander details block for a movie."""
    with st.expander("ℹ️ Details"):
        if isinstance(details['rating'], (int, float)):
            st.markdown(
                f"<div class='rating-badge'>★ {details['rating']}/10 &nbsp;·&nbsp; {details['vote_count']:,} votes</div>",
                unsafe_allow_html=True,
            )
        if details['genres'] != 'N/A':
            badges = "".join(
                f"<span class='detail-badge'>{g.strip()}</span>"
                for g in details['genres'].split(',')
            )
            st.markdown(f"<div>{badges}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='margin:6px 0;'><span class='detail-badge'>📅 {details['year']}</span>"
            f"<span class='detail-badge'>⏱ {details['runtime']}</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"<div class='overview-text'>{details['overview']}</div>", unsafe_allow_html=True)


# ── UI ─────────────────────────────────────────────────────────────────────────
movie_list = movies['title'].values
selected_movie = st.selectbox("🔎 Search or select a movie", movie_list)

if st.button("Recommend Movies"):
    with st.spinner("Finding similar movies... 🎥"):
        recommended_movies = recommend(selected_movie)

    # Fetch selected movie details
    sel_index = movies[movies['title'] == selected_movie].index[0]
    sel_id = movies.iloc[sel_index].movie_id
    selected_details = fetch_movie_details(sel_id)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Selected Movie (Top Section) ────────────────────────────────────────────
    st.markdown(
        "<h3 style='color: var(--gold); letter-spacing: 2px; margin-bottom: 20px;'>✨ YOUR SELECTION</h3>",
        unsafe_allow_html=True,
    )
    
    col_sel_img, col_sel_info = st.columns([1.5, 2], gap="large")
    
    with col_sel_img:
        st.image(selected_details['poster'], use_container_width=True)
    
    with col_sel_info:
        st.markdown(
            f"<h2 style='color: var(--text); margin: 0 0 12px 0;'>{selected_details['title']}</h2>",
            unsafe_allow_html=True,
        )
        if isinstance(selected_details['rating'], (int, float)):
            st.markdown(
                f"<div class='rating-badge'>★ {selected_details['rating']}/10 &nbsp;·&nbsp; {selected_details['vote_count']:,} votes</div>",
                unsafe_allow_html=True,
            )
        if selected_details['genres'] != 'N/A':
            badges = "".join(
                f"<span class='detail-badge'>{g.strip()}</span>"
                for g in selected_details['genres'].split(',')
            )
            st.markdown(f"<div style='margin-bottom: 12px;'>{badges}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='margin-bottom: 12px;'><span class='detail-badge'>📅 {selected_details['year']}</span>"
            f"<span class='detail-badge'>⏱ {selected_details['runtime']}</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='overview-text' style='border-top: 1px solid #333; padding-top: 12px; margin-top: 12px;'>{selected_details['overview']}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Recommendations Grid (5 columns) ────────────────────────────────────────
    st.markdown(
        "<h3 style='color: var(--gold); letter-spacing: 2px; margin-bottom: 20px;'>🎯 RECOMMENDED FOR YOU</h3>",
        unsafe_allow_html=True,
    )
    
    rec_cols = st.columns(5, gap="large")
    
    for i, rec in enumerate(recommended_movies):
        with rec_cols[i]:
            st.markdown(f"<div class='col-section-label'>#{i+1}</div>", unsafe_allow_html=True)
            st.image(rec['poster'], use_container_width=True)
            st.markdown(
                f"<div class='movie-label'><p>{rec['title']}</p></div>",
                unsafe_allow_html=True,
            )
            render_details(rec)

st.caption("Developed with ❤️ By Navneet")
