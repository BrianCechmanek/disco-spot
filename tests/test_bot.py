import pytest

from disco_spot.bot import (
    Config,
    DiscoBot
)


def test_Config_from_environment_variables(monkeypatch):
    # Set environment variables for testing
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "your_discord_token")
    monkeypatch.setenv("YOUTUBE_API_KEY", "your_youtube_api_key")
    monkeypatch.setenv("SPOTIPY_CLIENT_ID", "your_spotipy_client_id")
    monkeypatch.setenv("SPOTIPY_CLIENT_SECRET", "your_spotipy_client_secret")
    monkeypatch.setenv("SPOTIPY_REDIRECT_URI", "your_spotipy_redirect_uri")
    monkeypatch.setenv("SPOTIFY_USERNAME", "your_spotify_username")
    monkeypatch.setenv("PLAYLIST_ID", "your_playlist_id")

    # Create an instance of Config
    config = Config()

    # Check if values are correctly set
    assert config.DISCORD_BOT_TOKEN == "your_discord_token"
    assert config.YOUTUBE_API_KEY == "your_youtube_api_key"
    assert config.SPOTIPY_CLIENT_ID == "your_spotipy_client_id"
    assert config.SPOTIPY_CLIENT_SECRET == "your_spotipy_client_secret"
    assert config.SPOTIPY_REDIRECT_URI == "your_spotipy_redirect_uri"
    assert config.SPOTIFY_USERNAME == "your_spotify_username"
    assert config.PLAYLIST_ID == "your_playlist_id"


class TestDiscoBot:
    @pytest.mark.parametrize("text, expected",  [
        ("https://www.youtube.com/watch?v=6JYIGclVQdw", (True, "6JYIGclVQdw"),),
        ("this text has no link", (False, None)),
        ("this text has a link https://www.youtube.com/watch?v=U7mPqycQ0tQ", (True, "U7mPqycQ0tQ"),)
    ])
    def test_content_has_youtube_link(self, text, expected):
        res = DiscoBot.content_has_youtube_link(text)
        assert res == expected
