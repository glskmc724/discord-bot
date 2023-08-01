# Overview

Iron bot is a Discord bot using [discord.py](https://discordpy-ko.github.io/) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

When we use Iron bot, we need to get bot’s token and data API from [Discord](https://discord.com/developers/applications) and [Google](https://console.cloud.google.com/marketplace/product/google/youtube.googleapis.com).

We can use Iron bot for playing youtube video in discord voice channel, and can listen with our friends or companions.

# Installation

Run `git clone https://github.com/glskmc724/iron-bot`

## Windows

Preparing…

## Ubuntu

Iron bot tested on Ubuntu 20.04 LTS amd64 with Python 3.8.10.

To use Iron bot, we need to install Python packages discord, yt-dlp, pynacl using pip.

Also, we must install Ubuntu package ffmpeg using apt.

In the terminal, enter the command and press enter:

```bash
iron@iron:~$ pip install discord
iron@iron:~$ pip install yt-dlp
iron@iron:~$ pip install pynacl
iron@iron:~$ sudo apt-get install ffmpeg
```

# Settings

For use Iron bot, we must get Discord bot token and Youtube API key.

When we get the token and API key, insert `bot.conf` and save file.

```bash
# Input your discord bot token from https://discord.com/developers/application
discord_bot_token="Insert your bot's token"

# Input your youtube api key from https://consoke.cloud.google.com/apis/api/youtube.googleapis.com/
youtube_api_key="Insert your API key"
```

Iron bot support multiple channel but for use this function, we need to insert channel id in `channels.list` file. (Also need setting, when we use only single channel.)

```bash
# Input channel id
Insert your channel id from Discord server. only number.
```

We can get channel id from Discord server like below image. For get the channel id, we need to set developer mode in Discord app.


![image](https://github.com/glskmc724/iron-bot/assets/90677740/8c3a033b-6be1-4d0e-8c79-b8fa123c520b)

# Using


When installation completed, run `python3 iron_bot.py` for start bot.

If you want to using in background, run `nohup python3 iron_bot.py &`

### Credits


- [kmc000724@gmail.com](https://github.com/glskmc724), Using discord.py and yt-dlp.
- [@JHni2](https://github.com/JHni2), Get youtube video from Youtube Data API v3.
