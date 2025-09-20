import pytest

from disco_spot.bot import Config, DiscoBot


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
    @pytest.mark.parametrize(
        "text, expected",
        [
            (
                "https://www.youtube.com/watch?v=6JYIGclVQdw",
                (True, "6JYIGclVQdw"),
            ),
            ("this text has no link", (False, None)),
            (
                "this text has a link https://www.youtube.com/watch?v=U7mPqycQ0tQ",
                (True, "U7mPqycQ0tQ"),
            ),
        ],
    )
    def test_content_has_youtube_link(self, text, expected):
        res = DiscoBot.content_has_youtube_link(text)
        assert res == expected

    @pytest.mark.parametrize(
        "text, expected",
        [
            (
                "https://open.spotify.com/track/3ngS3O329Q5gn1Rn9r4q73",
                "3ngS3O329Q5gn1Rn9r4q73",
            ),
            (
                "https://open.spotify.com/track/3ghJMGcXyochkLaCXS0Fw1?si=856f4c7400b948ce",
                "3ghJMGcXyochkLaCXS0Fw1",
            ),
            ("this text has no spotify link", None),
        ],
    )
    def test_content_has_spotify_uri(self, text, expected):
        res = DiscoBot.content_has_spotify_uri(text)
        assert res == expected

    def test_add_track_to_playlist_success(monkeypatch):
        bot = DiscoBot()

        class DummySpotify:
            def __init__(self):
                self.called_with = None

            def playlist_add_items(self, playlist_id, items):
                self.called_with = (playlist_id, items)
                return True

        dummy = DummySpotify()
        bot.sp = dummy
        track_uri = "spotify:track:123"
        result = bot.add_track_to_playlist(track_uri)

        assert result is True
        assert dummy.called_with == (bot.config.PLAYLIST_ID, [track_uri])

    def test_add_track_to_playlist_failure(monkeypatch):
        bot = DiscoBot()

        class FailingSpotify:
            def playlist_add_items(self, playlist_id, items):
                raise Exception("API error")

        bot.sp = FailingSpotify()
        result = bot.add_track_to_playlist("spotify:track:123")
        assert result is False

    def test_add_by_yt_id_success(monkeypatch):
        bot = DiscoBot()

        # Patch yt_api.get_video_by_id
        class DummyYT:
            def get_video_by_id(self, video_id):
                class Video:
                    items = [
                        type(
                            "obj",
                            (),
                            {"snippet": type("obj", (), {"title": "Test Song"})},
                        )
                    ]

                return Video()

        bot.yt_api = DummyYT()

        # Patch sp.search
        class DummySpotify:
            def search(self, q, type, limit):
                return {
                    "tracks": {
                        "items": [
                            {
                                "uri": "spotify:track:123",
                                "name": "Test Song",
                                "artists": [{"name": "Test Artist"}],
                            }
                        ]
                    }
                }

            def track(self, uri):
                return {"name": "Test Song"}

            def playlist_add_items(self, playlist_id, items):
                return True

        bot.sp = DummySpotify()
        result = bot.add_by_yt_id("fake_yt_id")

        assert result == "Test Song"

    def test_add_by_yt_id_no_spotify_match(monkeypatch):
        bot = DiscoBot()

        class DummyYT:
            def get_video_by_id(self, video_id):
                class Video:
                    items = [
                        type(
                            "obj",
                            (),
                            {"snippet": type("obj", (), {"title": "Unknown Song"})},
                        )
                    ]

                return Video()

        bot.yt_api = DummyYT()

        class DummySpotify:
            def search(self, q, type, limit):
                return {"tracks": {"items": []}}

        bot.sp = DummySpotify()
        result = bot.add_by_yt_id("fake_yt_id")

        assert result is None
