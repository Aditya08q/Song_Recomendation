
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
st.title("YouTube Music Recommender")

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
    st.markdown("### Recommended Songs:")
    recommendations = recommend(selected_song)

    for song in recommendations:
        st.write(f"**{song['song']}** by *{song['artist']}*")
        if song["url"]:
            st.video(song["url"])  # Play YouTube video
        else:
            st.warning("No valid YouTube URL available for this song.")
