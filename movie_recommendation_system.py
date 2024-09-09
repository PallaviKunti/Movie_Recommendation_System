import streamlit as st
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
df=pd.read_csv('final_data.csv')

cv=CountVectorizer()
arr=cv.fit_transform(df.combined_features)
cs=cosine_similarity(arr)



def get_name(index_val):
    return df.loc[index_val].title
def get_id(index_val):
    return df.loc[index_val].id
def get_index(movie):
        try:
            return(df.index[df.title==movie])
        except:
            return 0

#st.title("Movie Recommendation System")

api_key = 'AIzaSyA3jLT4ydXGM1jCq_tccK2KIdthliCpUgM'

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    return data

def fetch_trailer(moviename):
    url = "https://www.googleapis.com/youtube/v3/search?part=snippet&key=AIzaSyA3jLT4ydXGM1jCq_tccK2KIdthliCpUgM&type=video&q="+moviename+" official trailer"
    mov_data = requests.get(url)
    mov_data = mov_data.json()
    for i in mov_data['items']:
        id= i['id']['videoId']
        return id


def recommend(selected):
    movie_index=get_index(selected)
    all_movies=list(enumerate(cs[movie_index[0]]))

    sorted_movie_indexes=sorted(all_movies,key=lambda x : x[1],reverse=True)

    recommend_movies_posters=[]
    recommend_movies_imbd=[]
    recommend_movies_overview=[]
    recommend_movies_names=[]
    recommend_movies_trailers=[]
    total=0
    for movie_ in sorted_movie_indexes:
        if(total<6):
            try:
                data = fetch_poster(get_id(movie_[0]))
                poster_path = data["poster_path"]
                path = "https://image.tmdb.org/t/p/w500/" + poster_path
                recommend_movies_posters.append(path)
                recommend_movies_imbd.append(data['vote_average'])
                recommend_movies_overview.append(data['overview'])
                recommend_movies_names.append(data['title'])
                video_id=fetch_trailer(get_name(movie_[0]))
                recommend_movies_trailers.append("http://youtube.com/embed/"+video_id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                total+=1
            except:
                pass
    
    col1, col2 = st.columns(2)
    with col1:
        st.header(recommend_movies_names[0])
        st.image(recommend_movies_posters[0])
        
    with col2:
        st.header(f"IMDB : {recommend_movies_imbd[0]}")
        st.write(f"Description : {recommend_movies_overview[0]}")
        st.subheader("Trailer")
        try:
            st.video(recommend_movies_trailers[0])
        except:
            pass
    
    st.header("Recommended Movies")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.write()
        st.write(recommend_movies_names[1])
        st.image(recommend_movies_posters[1])
        st.write(f"[Trailer]({recommend_movies_trailers[1]})")
    with col2:
        st.write(recommend_movies_names[2])
        st.image(recommend_movies_posters[2])
        st.write(f"[Trailer]({recommend_movies_trailers[2]})")
    with col3:
        st.write(recommend_movies_names[3])
        st.image(recommend_movies_posters[3])
        st.write(f"[Trailer]({recommend_movies_trailers[3]})")
    with col4:
        st.write(recommend_movies_names[4])
        st.image(recommend_movies_posters[4])
        st.write(f"[Trailer]({recommend_movies_trailers[4]})")
    with col5:
        st.write(recommend_movies_names[5])
        st.image(recommend_movies_posters[5])
        st.write(f"[Trailer]({recommend_movies_trailers[2]})")

st.sidebar.image('logo.png')

st.sidebar.title("Select a Movie")

movie_names = []
for i in range(4800):
    movie_names.append(get_name(i))

selected=st.sidebar.selectbox('Choose',movie_names)
if st.sidebar.button('Recommend'):
    recommend(selected)
