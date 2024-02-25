# minimal discord bot to read messages with "youtube" in them
# see examples for further functionality https://github.com/spotipy-dev/spotipy/tree/master/examples

from dotenv import load_dotenv
import logging
import logging.handlers
from pydantic_settings import BaseSettings
import re
import sys

import discord
from discord.ext import commands
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from pyyoutube import Api  # https://console.cloud.google.com/apis/credentials?)


# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# logging.getLogger('discord.http').setLevel(logging.ERROR)
logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.debug("Starting bot -- logging works")


class Config(BaseSettings):
    DISCORD_BOT_TOKEN: str
    YOUTUBE_API_KEY: str
    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str
    SPOTIPY_REDIRECT_URI: str
    SPOTIFY_USERNAME: str
    PLAYLIST_ID: str

    class ConfigDict:
        env_prefix = ""


class DiscoBot:
    # discord client
    intents = discord.Intents.default()
    intents.message_content = True
    scope = "playlist-modify-private"

    def __init__(self):
        self.config = Config()
        self.client = discord.Client(intents=self.intents)
        self.yt_api = Api(api_key=self.config.YOUTUBE_API_KEY)
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.config.SPOTIPY_CLIENT_ID,
                client_secret=self.config.SPOTIPY_CLIENT_SECRET,
                scope=self.scope,
            )
        )

    def start(self):
        bot = commands.Bot(command_prefix="!", intents=self.intents)
        bot.add_listener(self.on_ready, "on_ready")
        bot.add_listener(self.on_message, "on_message")
        bot.run(self.config.DISCORD_BOT_TOKEN)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We have logged in as {self.client.user}")

    @commands.Cog.listener()
    async def on_message(self, message):
        match message.author, message.channel.name, message.content:
            case self.client.user, _, _:
                return
            case _, _, _ if message.content.startswith("$hello"):
                await message.channel.send("Hello!")
                logging.info("Hello message received and responded to")
                return
            case (
                _,
                "music",
                _,
            ) if message.author.name == "sceptre" and "wild wild" in message.content.lower():
                await message.channel.send("I can't let you do that, Dave.")
                return
            case _, "music", _:
                is_yt, *yt_id = self.content_has_youtube_link(message.content)
                if is_yt:
                    res = self.add_by_yt_id(yt_id)
                    if res:
                        await message.channel.send(f"Added {res} to playlist")
                else:
                    print("No Action for message : ", message.content)
                    # print(f"{message.author = }")
                    # print(f"{message.channel.name = }")
                    # print(f"{message.content = }")
                    # print(f"{'wild' in message.content.lower() = }")
                return
            case _:
                return

    @staticmethod
    def content_has_youtube_link(content: str) -> tuple[bool, str | None]:
        # Regular expression to match YouTube URLs
        youtube_regex = r"(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
        youtube_match = re.search(youtube_regex, content)
        if youtube_match:
            video_id = youtube_match.group(6)
            print(f"{video_id = }")
            print("message.content has YOUTUBE: ", youtube_match.group())
            return True, video_id
        else:
            return (False, None)

    def get_title_from_yt_link(self, yt_id: str) -> str:
        """Use the yt to get the video title from the id. assume it is a song, for now"""
        # This pastebin https://pastebin.com/Dy7eUFdS
        # may have a short-circuit to title and artist, if we wanna try.
        video = self.yt_api.get_video_by_id(video_id=yt_id)
        return video.items[0].snippet.title

    def get_spotify_uri_from_title(self, yt_title: str) -> str | None:
        results = self.sp.search(q=yt_title, type="track", limit=1)

        tracks = results["tracks"]["items"]
        if tracks:
            track = tracks[0]
            print(f"Track Name: {track['name']}, Artist: {track['artists'][0]['name']}")
            return track["uri"]
        else:
            print("No tracks found.")
            return None

    def add_track_to_playlist(self, track_uri: str) -> bool:
        # Given a validated song, add it to the playlist
        try:
            self.sp.playlist_add_items(self.config.PLAYLIST_ID, [track_uri])
        except Exception as e:
            print(f"Error adding track to playlist: {e}")
            return False
        return True

    def get_spotify_title_from_uri(self, spotify_uri: str) -> str:
        """Get the title of the song from the uri"""
        return self.sp.track(spotify_uri)["name"]

    def add_by_yt_id(self, yt_id: str) -> str | None:
        """Try to add a song, and return the track title added. maybe spotify url too?"""
        if yt_title := self.get_title_from_yt_link(yt_id):
            if spotify_uri := self.get_spotify_uri_from_title(yt_title):
                spotify_title = self.get_spotify_title_from_uri(spotify_uri)
                self.add_track_to_playlist(spotify_uri)
                return spotify_title
            else:
                return f"No Spotify URI found for title: {yt_title}"
        else:
            print("No title found for video: ", yt_id)


def main():
    bot = DiscoBot()  # bot.client.run(token=config.DISCORD_BOT_TOKEN, log_handler=None)
    bot.start()


if __name__ == "__main__":
    # force load .env file -- TODO can remove if dockerized and env vars are set
    load_dotenv()
    main()
