# import pickle
# import streamlit as st
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# CLIENT_ID = "5c5f149ef0ca47ba9fc30f38c798020f"
# CLIENT_SECRET = "63557fca1f3e4ca1a4cd803ba4b3e881"

# # Initialize the Spotify client
# client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# def get_song_album_cover_url(song_name, artist_name):
#     search_query = f"track:{song_name} artist:{artist_name}"
#     results = sp.search(q=search_query, type="track")

#     if results and results["tracks"]["items"]:
#         track = results["tracks"]["items"][0]
#         album_cover_url = track["album"]["images"][0]["url"]
#         print(album_cover_url)
#         return album_cover_url
#     else:
#         return "https://i.postimg.cc/0QNxYz4V/social.png"

# def recommend(song):
#     index = music[music['song'] == song].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_music_names = []
#     recommended_music_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         artist = music.iloc[i[0]].artist
#         print(artist)
#         print(music.iloc[i[0]].song)
#         recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
#         recommended_music_names.append(music.iloc[i[0]].song)

#     return recommended_music_names,recommended_music_posters

# st.header('Music Recommender System')
# music = pickle.load(open('df.pkl','rb'))
# similarity = pickle.load(open('similarity.pkl','rb'))

# music_list = music['song'].values
# selected_movie = st.selectbox(
#     "Type or select a song from the dropdown",
#     music_list
# )

# if st.button('Show Recommendation'):
#     recommended_music_names,recommended_music_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5= st.columns(5)
#     with col1:
#         st.text(recommended_music_names[0])
#         st.image(recommended_music_posters[0])
#     with col2:
#         st.text(recommended_music_names[1])
#         st.image(recommended_music_posters[1])

#     with col3:
#         st.text(recommended_music_names[2])
#         st.image(recommended_music_posters[2])
#     with col4:
#         st.text(recommended_music_names[3])
#         st.image(recommended_music_posters[3])
#     with col5:
#         st.text(recommended_music_names[4])
#         st.image(recommended_music_posters[4])

# 



# yt
import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Load data
with open("df_yt.pkl", "rb") as f:
    df = pickle.load(f)

with open("similarity_yt.pkl", "rb") as f:
    similarity = pickle.load(f)

# Title
st.title("🎵 YouTube Music Recommender")

# Search box for user to pick a song
song_list = df['song'].dropna().unique()
selected_song = st.selectbox("Select a song to get similar recommendations:", sorted(song_list))

# Function to recommend songs
def recommend(song_name, top_n=5):
    try:
        index = df[df['song'] == song_name].index[0]
    except IndexError:
        return []

    distances = similarity[index]
    song_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:top_n+1]

    recommended = []
    for i, _ in song_indices:
        entry = df.iloc[i]
        recommended.append({
            "song": entry["song"],
            "artist": entry["artist"],
            "url": entry["youtube_url"] if isinstance(entry["youtube_url"], str) and entry["youtube_url"].startswith("http") else None
        })
    return recommended

# Show recommendations
if selected_song:
    st.markdown("### 🎧 Recommended Songs:")
    recommendations = recommend(selected_song)

    for song in recommendations:
        st.write(f"**{song['song']}** by *{song['artist']}*")
        if song["url"]:
            st.video(song["url"])  # Play YouTube video
        else:
            st.warning("⚠️ No valid YouTube URL available for this song.")
