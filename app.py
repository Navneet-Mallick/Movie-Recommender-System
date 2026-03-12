import pickle
import streamlit as st
import requests

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------- HEADER ----------
st.title("🎬 Movie Recommender System")
st.subheader("👨‍💻 Developed by Navneet Mallick")
st.write("")  # empty line for spacing

# ---------- LOAD DATA ----------
movies = pickle.load(open('models/movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# ---------- FUNCTION TO FETCH POSTER ----------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b8b7f8b9e3e9d3b0ab494f8f184edee&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ---------- FUNCTION TO RECOMMEND MOVIES ----------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # top 5 recommendations
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

# ---------- SHOW RECOMMENDATIONS ----------
if st.button('Recommend Movies'):
    with st.spinner("Finding similar movies... 🎥"):
        names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    # Display in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.write(names[i])
