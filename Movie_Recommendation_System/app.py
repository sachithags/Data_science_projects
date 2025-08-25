import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
        return recommended_movies
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return []

try:
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Data files not found. Please make sure 'movies.pkl' and 'similarity.pkl' are in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.markdown("""
    <h1 style='text-align: center; color: #1f77b4; margin-bottom: 20px;'>
        🎬 Movie Recommender System
    </h1>
""", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values
)

if st.button('Recommend', type='primary'):
    with st.spinner('Finding recommendations...'):
        recommendations = recommend(selected_movie_name)
        
        if recommendations:
            st.markdown(f"""
                <h3 style='text-align: center; margin-top: 25px; margin-bottom: 20px;'>
                    Because you liked: <span style='color: #ff4b4b;'>{selected_movie_name}</span>
                </h3>
            """, unsafe_allow_html=True)
            
            for i, movie in enumerate(recommendations, 1):
                st.markdown(f"""
                    <div style='
                        background-color: #7BDBCA;
                        border-radius: 8px;
                        padding: 10px;
                        margin: 8px 0;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        border-left: 4px solid #1f77b4;
                    '>
                        <p style='margin: 0; color: #333; font-size: 15px;'>
                            🎬 {movie}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Could not generate recommendations. Please try another movie.")