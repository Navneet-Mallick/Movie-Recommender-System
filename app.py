import pickle
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:#ff4b4b;
}

.dev-name{
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
}

.movie-title{
    text-align:center;
    font-size:16px;
    font-weight:600;
}

.stButton>button{
    width:100%;
    background-color:#ff4b4b;
    color:white;
    font-size:18px;
    border-radius:10px;
    height:3em;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<p class="main-title">🎬 Movie Recommender System</p>', unsafe_allow_html=True)
st.markdown('<p class="dev-name">Developed by <b>Navneet Mallick</b></p>', unsafe_allow_html=True)


# ---------- LOAD DATA ----------
movies = pickle.load(open('models/movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


# ---------- FETCH POSTER ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b8b7f8b9e3e9d3b0ab494f8f184edee&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/" + poster_path


# ---------- RECOMMEND FUNCTION ----------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# ---------- MOVIE SELECT ----------
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "🔎 Search or select a movie",
    movie_list
)

# ---------- BUTTON ----------
if st.button('Recommend Movies'):
    
    with st.spinner("Finding similar movies... 🎥"):
        names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(f"<p class='movie-title'>{names[i]}</p>", unsafe_allow_html=True)
