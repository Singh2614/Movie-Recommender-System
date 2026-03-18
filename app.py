import streamlit as st
import pandas as pd
import pickle
import requests

# Load your data and models
movies = pickle.load(open('movies.pkl','rb'))  # your preprocessed dataset
similarity = pickle.load(open('similarity.pkl', 'rb'))  # your similarity matrix

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=317d42aa9468e3e51a8a9465d72e8c8f&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie,num_recommendations=10):
    index = movies[movies['original_title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    posters = []
    for i in distances[1:num_recommendations+1]:
        movie_id=movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        posters.append(fetch_poster(movie_id))
    return recommended_movies, posters

# Streamlit UI
st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['original_title'].values
)

# User input for number of recommendations
num_recs = st.number_input(
    'How many recommendations do you want?',
    min_value=1,
    max_value=20,
    value=5,
    step=1
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie,num_recs)
    cols_per_row = 4

    for i in range(0, len(names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(names):
                with cols[j]:
                    st.text(names[i + j])
                    st.image(posters[i + j])

