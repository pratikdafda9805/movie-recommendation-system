import pandas as pd
import numpy as np
import pickle as pkl
import streamlit as st
import requests

def fetch_poster(movie_title):
    response = requests.get('http://www.omdbapi.com/?t={}&apikey={}'.format(movie_title,"83baee0b"))
    data = response.json()

    if data['Response'] == 'True':
        return data.get('Poster','')
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"
final = pd.read_csv('final.csv', index_col=0)
netflix = pd.read_csv('movies.csv', index_col=0)

similarity = pkl.load(open('similarity.pkl', 'rb'))

file = final.merge(netflix, on='title')

st.header('Netflix Movie Recommendation')
movie=st.selectbox('Select Movie', file['title'].sort_values())

def recommend(obj):
    movie_index = file[file['title']==obj].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    movies = []
    for i in movie_list:
        movies.append(file.iloc[i[0]].title)
    return movies

if st.button('Recommend'):
    if file[file['title'] == movie]['type'].iloc[0]=="['Movie']":
        st.header('Here is your Movie Recommendation')
    else:
        st.header('Here is your TV Shows Recommendation')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <img src="{fetch_poster(movie)}" 
            style="width:500px; height:480px; object-fit:cover; border-radius:10px;">
            """,
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="movie-title">{movie}</div>', unsafe_allow_html=True)

    with col2:
        cols = st.columns(2)
        movies = recommend(movie)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <img src="{fetch_poster(movies[idx])}" 
                    style="width:300px; height:250px; object-fit:cover; border-radius:5px;">
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(f'<div class="movie-title">{movies[idx]}</div>', unsafe_allow_html=True)
        col1 = st.columns(2)

        cols = st.columns(3)
        movies = recommend(movie)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(
                    f"""
                    <img src="{fetch_poster(movies[idx+2])}" 
                    style="width:200px; height:150px; object-fit:cover; border-radius:3px;">
                    """,
                    unsafe_allow_html=True
                )
                st.markdown(f'<div class="movie-title">{movies[idx+2]}</div>', unsafe_allow_html=True)
