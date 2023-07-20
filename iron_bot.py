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
    async def pause_callback(self, interaction):
        if (self.vc.is_playing()):
            self.vc.pause()
            await self.view_msg.edit(content = "Paused", view = await self.create_view())
        await interaction.response.defer()

    async def stop_callback(self, interaction):
        if (self.vc.is_playing() or self.vc.is_paused()):
            self.vc.stop()
        await interaction.response.defer()

    async def resume_callback(self, interaction):
        if (self.vc.is_paused()):
            self.vc.resume()
            await self.view_msg.edit(content = "Playing", view = await self.create_view())
        await interaction.response.defer()

    async def create_view(self):
        """ ⇄  ◁  II ▷ ↻ """
        pause_btn = Button(label = "II", style = ButtonStyle.secondary)
        pause_btn.callback = self.pause_callback
        stop_btn = Button(label = "□", style = ButtonStyle.secondary)
        stop_btn.callback = self.stop_callback
        resume_btn = Button(label = "▷", style = ButtonStyle.secondary)
        resume_btn.callback = self.resume_callback
        view = View()
        if (self.vc.is_paused()):
            view.add_item(resume_btn)
        else:
            view.add_item(pause_btn)
        view.add_item(stop_btn)

        return view

    async def create_content(self, youtube_content):
        title = youtube_content["snippet"]["title"]
        thumbnail = youtube_content["snippet"]["thumbnails"]["medium"]
        content = "{}\r\n{}".format(title, thumbnail["url"])
        return content

    async def on_ready(self):
        return;

    async def on_message(self, message):
        if (message.author == self.user):
            return

        """
        if (message.content == "!delete"):
            message.channel.purge(limit = 1000)
            return
        """

        if (verify_channel(message.channel.id) != True):
            return

        channel = self.get_channel(message.channel.id)
        #await channel.send(message.content)
        
        self.user_msg = message
        self.msgs = [self.user_msg]

        # find music
        res = youtube.search_api(message.content)
        vidid = res["items"][0]["id"]["videoId"]
        link = "https://www.youtube.com/embed/{}".format(vidid)
        song = youtube.download(link)

        # connect
        ch = self.get_channel(message.author.voice.channel.id)
        self.vc = await ch.connect()
        view = await self.create_view()
        content = await self.create_content(res["items"][0])
        self.view_msg = await channel.send(content = content, view = view)
        self.msgs.append(self.view_msg)

        self.vc.play(discord.FFmpegPCMAudio(executable = "ffmpeg", source = song))

        while self.vc.is_playing() or self.vc.is_paused():
            await asyncio.sleep(0.1)
        
        await self.vc.disconnect()
        for msg in self.msgs:
            await msg.delete()

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
