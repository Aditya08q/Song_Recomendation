import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load your YouTube music dataset
df = pd.read_csv("youtube_music.csv")  # make sure it has 'song', 'artist', 'youtube_url'

# Combine metadata for better recommendations
df["combined"] = df["song"] + " " + df["artist"] + " " + df.get("description", "")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["combined"])

# Cosine similarity matrix
similarity_matrix = cosine_similarity(tfidf_matrix)

# Save both to disk
pickle.dump(df, open("df_yt.pkl", "wb"))
pickle.dump(similarity_matrix, open("similarity_yt.pkl", "wb"))
