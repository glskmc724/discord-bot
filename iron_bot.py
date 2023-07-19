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
            async def resume_callback(interaction):
                if (vc.is_paused()):
                    vc.resume()
                await interaction.response.send_message("Resume")

            if (vc.is_playing()):
                vc.pause()

            resume_btn = Button(label = "Resume", style = ButtonStyle.primary)
            resume_btn.callback = resume_callback
            view = View()
            view.add_item(resume_btn)
            await interaction.response.send_message(view = view)

        async def stop_callback(interaction):
            if (vc.is_playing()):
                vc.stop()

        pause_btn = Button(label = "Pause", style = ButtonStyle.primary)
        pause_btn.callback = pause_callback
        stop_btn = Button(label = "Stop", style = ButtonStyle.primary)
        stop_btn.callback = stop_callback
        view = View()
        view.add_item(pause_btn)
        view.add_item(stop_btn)
        msg.append(await channel.send("Play Music...", view = view))

        # connect
        ch = self.get_channel(message.author.voice.channel.id)
        vc = await ch.connect()

        vc.play(discord.FFmpegPCMAudio(executable = "ffmpeg", source = song))

        while vc.is_playing() or vc.is_paused():
            await asyncio.sleep(0.1)
        
        await vc.disconnect()
        for i in msg:
            await i.delete()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
