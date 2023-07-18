import discord
import iron_token
import asyncio
import youtube

TOKEN = iron_token.TOKEN

def verify_channel(channel_id):
    filename = "channels.list"
    channel_list_file = open(filename, 'r')
    channel_list = channel_list_file.readlines()

    for channel in channel_list:
        if (channel[0] == '#'):
            continue
        elif (int(channel) == channel_id):
            return True
    return False

class Client(discord.Client):
    async def on_ready(self):
        return;

    async def on_message(self, message):
        if (message.author == self.user):
            return;

        if (verify_channel(message.channel.id) != True):
            return;

        #channel = self.get_channel(message.channel.id)
        #await channel.send(message.content)
        
        # find music
        res = youtube.search(message.content)
        link = res[0]['href']
        song = youtube.download(link)

        # connect
        ch = self.get_channel(message.author.voice.channel.id)
        vc = await ch.connect()

        vc.play(discord.FFmpegPCMAudio(executable = "ffmpeg", source = song))

        while vc.is_playing():
            await asyncio.sleep(0.1)
        
        await vc.disconnect()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
