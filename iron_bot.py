import discord
import iron_token
import asyncio
import youtube

TOKEN = iron_token.TOKEN
CHANNEL_ID = iron_token.CHANNEL_ID

class Client(discord.Client):
    async def on_ready(self):
        self.channel = self.get_channel(CHANNEL_ID)
        await self.channel.send("Hello World")

    async def on_message(self, message):
        if (message.author == self.user):
            return;

        if (message.channel.id != CHANNEL_ID):
            return;
        
        #await self.channel.send(message.content)

        ch = self.get_channel(message.author.voice.channel.id)
        vc = await ch.connect()
        
        res = youtube.search(message.content)
        link = res[0]['href']

        song = youtube.download(link)
        vc.play(discord.FFmpegPCMAudio(executable = "ffmpeg", source = song))

        while vc.is_playing():
            await asyncio.sleep(0.1)
        
        await vc.disconnect()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
