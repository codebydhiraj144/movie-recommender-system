import streamlit as st
import pickle
import pandas as pd
import requests

# TMDB API placeholder
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    if not movie_id or pd.isna(movie_id):
        return None
    url = f'https://api.themoviedb.org/3/movie/{int(movie_id)}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            return None
    except:
        return None

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie, num_recommendations=20):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:num_recommendations+1]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_row = movies.iloc[i[0]]
        movie_title = str(movie_row['title'])
        movie_id = movie_row['movie_id'] if 'movie_id' in movie_row else None

        poster = fetch_poster(movie_id)

        # ✅ Skip movies with missing posters
        if poster:
            recommended_movies.append(movie_title)
            recommended_posters.append(poster)

    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search for a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name, num_recommendations=30)  # fetch more, since some skipped
    st.subheader("Recommended Movies:")

    # Display 5 posters per row
    cols = st.columns(5)
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with cols[idx % 5]:
            st.image(poster, use_container_width=True)
            st.caption(name)
