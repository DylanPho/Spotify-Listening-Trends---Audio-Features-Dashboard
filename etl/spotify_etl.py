import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Authenticate with client credentials (public data only)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
))

def fetch_playlist_tracks(playlist_id):
    print(f"Fetching tracks from playlist: {playlist_id}")
    
    # Initial request with market parameter
    results = sp.playlist_tracks(playlist_id, market="US")
    tracks = results['items']

    # Pagination: fetch next pages
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_data = []

    for item in tracks:
        track = item['track']
        if not track: continue  # Skip if track is None

        audio_features = sp.audio_features(track['id'])[0]
        if not audio_features: continue  # Skip if audio features are unavailable

        track_data.append({
            'track_name': track['name'],
            'artist': track['artists'][0]['name'],
            'popularity': track['popularity'],
            'danceability': audio_features['danceability'],
            'energy': audio_features['energy'],
            'tempo': audio_features['tempo'],
            'duration_ms': audio_features['duration_ms']
        })

    return pd.DataFrame(track_data)

def save_to_sqlite(df, db_path="../data/spotify.db"):
    print("Saving to SQLite database...")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql("spotify_tracks", engine, if_exists='replace', index=False)
    print(f"Saved {len(df)} tracks to {db_path}")

if __name__ == "__main__":
    playlist_id = "0I0YiGfPrZtlzu1z4wHtoC" # indie chill wanderlust
    
    df = fetch_playlist_tracks(playlist_id)

    if df.empty:
        print("No tracks were fetched. Please check the playlist ID or API permissions.")
    else:
        print(df.head())
        save_to_sqlite(df)
