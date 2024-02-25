# disco-spot

A friendly discord bot to help add youtube music links to a spotify playlist.

# Installation & Development

* I made this on Windows and I'm really _really_ lazy. So it uses conda
* So just run `conda env create -f environment.yml` and it'll set you up. Don't like it? want to use `pdm`? Sure, man. I'm not a cop
* I added in [pre-commit](https://pre-commit.com/) for all your isort/black/ruff needs

# Setup & Running

* You need to create a `.env` file like `.env.example`(this uses `python-dotenv` to load up the `.env` file and `os.getenv(<TOKEN>)` to actually read the env vars)
* I'll hopefully move the .env stuff out during dockerizing
* You need to manually invite the bot to your server. for dev work, I've created my own server "Mumps Test Server", feel free to ask me for an invite to it. For your own, follow [these steps](https://discordpy.readthedocs.io/en/stable/discord.html#inviting-your-bot) (**For Doto Channel, I don't have “Manage Server” permissions**. Until bot is ready I won't worry about going there)

## Requirements.lock

Conda, turns out, sorta sucks for requirements files. Or I just don't know how to use it. Or both. So I just manually make a `requirements.lock` file and commit that. Update it manually if you change any packages.

`conda list -e > requirements.lock`

## Running

1. download this repo
2. get all of the appropriate keys/tokens as in `.env.example`
3. make/activate a venv
4. run `python src/disco_spot/bot.py` (tbd: Dockerfile...)

## Deployment

Because Spotify is super dev hostile, deployment is a bit awkward: an Oauth login is required via a browser opening. Once logged in, a `.cache` file is created and should maintain login state. **Thus**, the bot must be run local, to log in, and then the `.cache` can be copied and sent into the headless bot.




# Issues

So many, dude. But, baby steps

* It only reads new messages (`on_message`)
* No archival reading: no idea how
* No server - run it locally ~~(I'm considering what the cheapest lambda or fargate server setup could be. I don't have an open IP to run from as of rn)~~ (see dockerizing. I'll run from my homelab/Portainer)
* ~~it stupidly grabs any \*.youtube.\* link. no processing for songs et c yet. or those weird you~~ regex game is strong
* ~~no pyproject.toml yet~~ installs via `setuptools` (hatch? rye?)
* logging is all bodged - I just want a streamhandler to stdout. Un-muting the dicord.http logging is a _mess_
* ~~Using python `3.12` appears to be a mess as well (setuptools, pip); likely downgrade to 3.11~~ Done. 3.11 fixes pre-commit

# TODOs

(Per Davey's handy dandy roadmap)

1. ~~watch discord channel for youtube links (with a discord bot)~~
2. ~~fetch the html content of the youtube link~~ not needed. though may lead to better matching: https://pastebin.com/Dy7eUFdS
3. ~~parse the html for the Open Graph title (what discord uses to generate the link previews)~~ I was never gonna do this anyway
4. ~~look for some sort of meta tag to try and figure out if the posted video is a song.~~
5. remove duplicate versions of wild wild west
6. ~~interact with spotify api to add song title to playlist.~~ works! logging in sucks though
7. Dockerize
8. Launch and run-with-restart on lab/Portainer
