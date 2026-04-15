import streamlit as st
import pickle
import requests
movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('simimlarity.pkl','rb'))
movies_list = movies['title'].values
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a011daec76d8e9cbb97ba024a402540f&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    listmovie = []
    poster = []
    for i in movie_list:
        movie_id = i[0]
        listmovie.append(movies.iloc[i[0]].title)
        poster.append(fetch_poster(movie_id))
    return listmovie,poster
st.title("movies recomandation")
options = st.selectbox("Enter the name of the movie ",movies_list)
if st.button("recommend"):
    name,poster = recommended(options)
    for i in name:
          st.text(i)
          st.image(poster[0])

