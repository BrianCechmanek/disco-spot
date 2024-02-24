import pytest

from disco_spot.bot import (
    get_title_from_yt_link,
    get_spotify_uri_from_title,
    content_has_youtube_link,
)

@pytest.parametrize("text", [("https://www.youtube.com/watch?v=6JYIGclVQdw", (True, "6JYIGclVQdw"),),
                             ("this text has no link", (False, None)),
                             ("this text has a link https://www.youtube.com/watch?v=U7mPqycQ0tQ", (True, "U7mPqycQ0tQ"),)
                             ])
def test_content_has_youtube_link(text, expected):
    res = content_has_youtube_link(text)
    assert res == expected