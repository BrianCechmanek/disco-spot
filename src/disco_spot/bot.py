# minimal discord bot to read messages with "youtube" in them

from dotenv import load_dotenv
import logging
import logging.handlers
import os
import re
import sys

import discord
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from pyyoutube import Api   # https://console.cloud.google.com/apis/credentials?)


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

# ENV VARS
load_dotenv()  # will search for .env file in local folder and load variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIFY_USERNAME= os.getenv("SPOTIFY_USERNAME")
PLAYLIST_ID="1vZfee7pkUhQuAC3CUnKUY"

# discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# youtube client
yt_api = Api(api_key=os.environ['YOUTUBE_API_KEY'])

# Set up Spotify API
# scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'], 
                                                           client_secret=os.environ['SPOTIPY_CLIENT_SECRET']))


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    # TODO swap in match case
    if message.author == client.user:
        return
    if not message.channel.name == "music":
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")
        # print(f"message : {message.content}\nchannel: {message.channel}\n author: {message.author}\n server: {message.guild.name}")
        logging.info("Hello message received and responsed to")
        return
    
    # begin check sequences
    is_yt, yt_id = content_has_youtube_link(message.content)
    if is_yt:
        await message.channel.send(
            """I see you posted a YouTube link. I'm currently
                                   working on a feature to get songs into a Spotify playlist.
                                   Stay tuned"""
        )
        logging.info(
            f"yt message : {message.content}\nchannel: {message.channel}\n author: {message.author}\n server: {message.guild.name}"
        )
        yt_title = get_title_from_yt_link(yt_id)
        spotify_uri = get_spotify_uri_from_title(yt_title)
        if spotify_uri:
            add_track_to_playlist(spotify_uri)
            await message.channel.send(f"Added {yt_title} to the playlist. If this is wrong. thumbs down. I'll work on removing it")
        else:
            print("No Spotify URI found for song: ", yt_title)


    else:
        print("No Action for message : ", message.content)


def content_has_youtube_link(content: str) -> tuple[bool, str|None]:
    # Regular expression to match YouTube URLs
    youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    youtube_match = re.search(youtube_regex, content)
    if youtube_match:
        video_id = youtube_match.group(6)
        print(f"{video_id = }")
        print("message.content has YOUTUBE: ", youtube_match.group())
        return True, video_id
    else:
        False, None


def get_title_from_yt_link(yt_id: str, api=yt_api) -> str:
    """Use the yt API to get the video title from the id. assume it is a song, for now"""
    # This pastebin https://pastebin.com/Dy7eUFdS 
    # may have a short-circuit to title and artist, if we wanna try. 
    video = api.get_video_by_id(video_id=yt_id)
    return video.items[0].snippet.title


def get_spotify_uri_from_title(yt_title: str) -> str|None:
    results = sp.search(q=yt_title, type='track', limit=1)

    tracks = results['tracks']['items']
    if tracks:
        track = tracks[0]
        print(f"Track Name: {track['name']}, Artist: {track['artists'][0]['name']}")
        return track['uri']
    else:
        print("No tracks found.")
        return None


def add_track_to_playlist(track_uri: str):
    # Given a validated song, add it to the playlist
    ...


def main(client, sp, yt_api):
    # Suppress the default configuration since we have our own
    client.run(token=DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main(client)
