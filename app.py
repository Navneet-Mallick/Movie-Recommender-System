import pickle
import streamlit as st
import requests
import time  # just to simulate progress (optional)

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.title("🎬 Movie Recommender System")
st.write("")

# Load data
movies = pickle.load(open('models/movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

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

    # Get selected movie poster
    selected_index = movies[movies['title'] == selected_movie].index[0]
    selected_movie_id = movies.iloc[selected_index].movie_id
    selected_poster = fetch_poster(selected_movie_id)
    
    # Professional header
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
        <h2 style='color: white; margin: 0;'>✨ Recommended Movies Based On</h2>
        <h3 style='color: #FFD700; margin: 10px 0 0 0;'>{selected_movie}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Display recommendations first
    st.markdown("##### Top 5 Recommendations:")
    cols = st.columns(5, gap="medium")
    
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_column_width=True)
            st.markdown(f"""
            <div style='text-align: center; padding: 10px; background-color: #f0f2f6; 
                        border-radius: 8px; margin-top: 10px;'>
                <p style='font-weight: bold; font-size: 13px; margin: 0; color: #000;'>{names[i]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Display selected movie at the bottom
    st.markdown("---")
    st.markdown("##### 🎬 Your Selection:")
    col_sel = st.columns([1, 2, 1])
    with col_sel[1]:
        st.image(selected_poster, use_column_width=True)
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background-color: #e8f4f8; 
                    border-radius: 8px; margin-top: 10px; border-left: 4px solid #667eea;'>
            <p style='font-weight: bold; font-size: 16px; margin: 0; color: #000;'>{selected_movie}</p>
        </div>
        """, unsafe_allow_html=True)
