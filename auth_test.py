from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="playlist-read-private playlist-read-collaborative"
))

playlist_id = "0I0YiGfPrZtlzu1z4wHtoC" # indie chill wanderlust

results = sp.playlist_tracks(playlist_id, market="US")
for i, item in enumerate(results['items']):
    track = item['track']
    print(f"{i+1}. {track['name']} by {track['artists'][0]['name']}")
