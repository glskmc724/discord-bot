import discord
import iron_token
import asyncio
import youtube

from discord.ui import Button, View
from discord import ButtonStyle

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

        channel = self.get_channel(message.channel.id)
        #await channel.send(message.content)
        
        msg = [message]

        # find music
        res = youtube.search(message.content)
        link = res[0]['href']
        song = youtube.download(link)

        async def pause_callback(interaction):
            if (vc.is_playing()):
                vc.stop()
            msg.append(await interaction.response.send_message("Pause music"))

        pause_btn = Button(label = "Pause", style = ButtonStyle.primary)
        pause_btn.callback = pause_callback
        view = View()
        view.add_item(pause_btn)
        msg.append(await channel.send("Play Music...", view = view))

        # connect
        ch = self.get_channel(message.author.voice.channel.id)
        vc = await ch.connect()

        vc.play(discord.FFmpegPCMAudio(executable = "ffmpeg", source = song))

        while vc.is_playing():
            await asyncio.sleep(0.1)
        
        await vc.disconnect()
        for i in msg:
            await i.delete()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
