CREATE TABLE IF NOT EXISTS tunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    spotify_track_id TEXT NOT NULL,
    track_name TEXT NOT NULL,
    artist_name TEXT,
    album_name TEXT,
    spotify_url TEXT,
    discord_user_id TEXT,
    discord_user_name TEXT,
    youtube_url TEXT,
    youtube_title TEXT,
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
);