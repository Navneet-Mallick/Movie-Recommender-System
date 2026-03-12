import pickle
import streamlit as st
import requests
import time  # just to simulate progress (optional)

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.subheader("👨‍💻 Developed by Navneet Mallick")
st.write("")

# Load data
movies = pickle.load(open('models/movie_list.pkl','rb'))
similarity = pickle.load(open('models/similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=7b8b7f8b9e3e9d3b0ab494f8f184edee&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    recommended_movie_names = []
    recommended_movie_posters = []

    progress_bar = st.progress(0)  # initialize progress bar

    for i, val in enumerate(distances[1:6]):  # top 5
        movie_id = movies.iloc[val[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[val[0]].title)
        progress_bar.progress((i + 1)/5)  # update progress bar

    progress_bar.empty()  # remove progress bar when done
    return recommended_movie_names, recommended_movie_posters

movie_list = movies['title'].values
selected_movie = st.selectbox("🔎 Search or select a movie", movie_list)

if st.button("Recommend Movies"):
    with st.spinner("Finding similar movies... 🎥"):
        names, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.write(names[i])
