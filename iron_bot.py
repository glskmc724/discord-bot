import discord
import iron_token
import time

TOKEN = iron_token.TOKEN
CHANNEL_ID = iron_token.CHANNEL_ID


class Client(discord.Client):
    async def on_ready(self):
        self.channel = self.get_channel(CHANNEL_ID)
        await self.channel.send("Hello World")

    async def on_message(self, message):
        if (message.author == self.user):
            return;
        await self.channel.send(message.content)

        ch = self.get_channel(message.author.voice.channel.id)
        vc = await ch.connect()

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=iron_token.SONG))

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
