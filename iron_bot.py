import discord
import iron_token
import asyncio
import youtube

from discord.ui import Button, View
from discord import ButtonStyle

TOKEN = iron_token.TOKEN

class Client(discord.Client):
    async def on_ready(self):
        pass

    async def on_message(self, message):
        if (message.author == self.user):
            return

if (__name__ == "__main__"):
    intents = discord.Intents.default()
    intents.message_content = True
    client = Client(intents=intents)
    client.run(TOKEN)
