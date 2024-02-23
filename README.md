# disco-spot

A friendly discord bot to help add youtube music links to a spotify playlist.

# Installation & Development

* I made this on Windows and I'm really _really_ lazy. So it uses conda
* So just run `conda env create -f environment.yml` and it'll set you up. Don't like it? want to use `pdm`? Sure, man. I'm not a cop
* I added in [pre-commit](https://pre-commit.com/) for all your isort/black/ruff needs

# Setup & Running

* You need to create a `.env` file and add a `DISCORD_BOT_TOKEN` to it **or** add that token to your environment however else you prefer (this uses `python-dotenv` to load up the `.env` file and `os.getenv(<TOKEN>)` to actually read the env vars)
* You need to manually invite the bot to your server. for dev work, I've created my own server "Mumps Test Server", feel free to ask me for an invite to it. For your own, follow [these steps](https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot) (**For Doto Channel, I don't have “Manage Server” permissions**. Until bot is ready I won't worry about going there)

# Issues

So many, dude. But, baby steps

* It only reads new messages (`on_message`)
* No archival reading: no idea how
* No server - run it locally (I'm considering what the cheapest lambda or fargate server setup could be. I don't have an open IP to run from as of rn)
* it stupidly grabs any \*.youtube.\* link. no processing for songs et c yet. or those weird you
* no pyproject.toml yet
* logging is all bodged - I just want a streamhandler to stdout. Un-muting the dicord.http logging is a _mess_
* ~~Using python `3.12` appears to be a mess as well (setuptools, pip); likely downgrade to 3.11~~ Done. 3.11 fixes pre-commit

# TODOs

(Per Davey's handy dandy roadmap)

1. ~~watch discord channel for youtube links (with a discord bot)~~
2. fetch the html content of the youtube link
3. parse the html for the Open Graph title (what discord uses to generate the link previews)
4. look for some sort of meta tag to try and figure out if the posted video is a song.
5. remove duplicate versions of wild wild west
6. interact with spotify api to add song title to playlist.