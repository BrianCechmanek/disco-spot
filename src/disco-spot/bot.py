# minimal discord bot to read messages with "youtube" in them

from dotenv import load_dotenv
import logging
import logging.handlers
import os
import sys

import discord
from discord.ext import commands

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

load_dotenv()  # will search for .env file in local folder and load variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# This example requires the 'message_content' intent.
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


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
    elif message_is_youtube_link(message):
        add_song_to_spotify(message.content)
        await message.channel.send(
            """I see you posted a YouTube link. I'm currently
                                   working on a feature to get songs into a Spotify playlist.
                                   Stay tuned"""
        )
        logging.info(
            f"yt message : {message.content}\nchannel: {message.channel}\n author: {message.author}\n server: {message.guild.name}"
        )
        return
    else:
        print("No Action for message : ", message.content)


def message_is_youtube_link(message) -> bool:
    if "youtube" in message.content.lower():
        print("message.content has YOUTUBE: ", message.content)
        return True
    else:
        False


def add_song_to_spotify(link: str):
    # if a yt link is found, go through verification steps
    # if it's a song, lookup open graph
    # if it's there, add it to spotify
    ...


def main(client):
    # Suppress the default configuration since we have our own
    client.run(token=DISCORD_BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main(client)
