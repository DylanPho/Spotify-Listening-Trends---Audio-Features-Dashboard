import os
import dotenv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

# Load environment variables from .env file
dotenv.load_dotenv()

# Set up authentication using SpotifyOAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-read-private user-library-read",
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
))

def fetch_playlist_tracks(playlist_id):
    print(f"Fetching tracks from playlist: {playlist_id}")
    results = sp.playlist_items(playlist_id, additional_types=['track'])
    tracks = results['items']

    # Continue fetching next pages
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    data = []

    for item in tracks:
        track = item.get('track')
        if not track:
            continue

        track_id = track['id']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        album_name = track['album']['name']
        release_date = track['album']['release_date']
        popularity = track['popularity']

        try:
            audio_features = sp.audio_features(track_id)[0]
            if audio_features is None:
                raise SpotifyException(403, -1, "Audio features not found")

            data.append({
                "track_id": track_id,
                "track_name": track_name,
                "artist_name": artist_name,
                "album_name": album_name,
                "release_date": release_date,
                "popularity": popularity,
                "danceability": audio_features["danceability"],
                "energy": audio_features["energy"],
                "key": audio_features["key"],
                "loudness": audio_features["loudness"],
                "mode": audio_features["mode"],
                "speechiness": audio_features["speechiness"],
                "acousticness": audio_features["acousticness"],
                "instrumentalness": audio_features["instrumentalness"],
                "liveness": audio_features["liveness"],
                "valence": audio_features["valence"],
                "tempo": audio_features["tempo"],
                "duration_ms": audio_features["duration_ms"],
                "time_signature": audio_features["time_signature"]
            })

        except SpotifyException as e:
            print(f"⚠️ Skipping track due to audio_features error: {track_name} ({track_id})")
            print(f"{e}")

    if not data:
        print("⚠️ No tracks were fetched. Check the playlist ID or API access.")
        return pd.DataFrame()

    return pd.DataFrame(data)

if __name__ == "__main__":
    playlist_id = "0I0YiGfPrZtlzu1z4wHtoC"  # Replace with your own playlist ID
    df = fetch_playlist_tracks(playlist_id)

    if not df.empty:
        os.makedirs("data", exist_ok=True)
        output_file = "data/spotify_audio_features.csv"
        df.to_csv(output_file, index=False)
        print(f"✅ Data saved to {output_file}")
    else:
        print("❌ No data to save.")
