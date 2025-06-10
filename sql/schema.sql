CREATE TABLE spotify_Tracks (
    id SERIAL PRIMARY KEY,
    track_name TEXT,
    artist TEXT,
    popularity INTEGER,
    danceability FLOAT,
    energy FLOAT,
    tempo FLOAT,
    duration_ms INTEGER
);