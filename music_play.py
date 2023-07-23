import discord
import youtube
import asyncio

class Music_Play:
    channel = 0
    video_id = ""
    repeat = False
    paused = False
    voice_client = None
    music_message = None
    playing = False
    queue = []
    queue_open = False
    loop = None
    playlist = []
    def __init__(self, channel = None, video_id = ""):
        self.channel = channel
        self.video_id = video_id

    async def loop_init(self):
        self.loop = asyncio.new_event_loop()
        
    def download(self):
        url = "https://www.youtube.com/embed/{}".format(self.video_id)
        self.music = youtube.download(url)

    async def repeat_callback(self, interaction):
        self.repeat = not self.repeat
        self.music_message.set_repeat(self.repeat)
        await self.music_message.update_music_message()
        await interaction.response.defer()

    async def paused_callback(self, interaction):
        self.paused = True
        self.voice_client.pause()
        self.music_message.set_paused(self.paused)
        await self.music_message.update_music_message()
        await interaction.response.defer()

    async def play_callback(self, interaction):
        self.paused = False
        self.voice_client.resume()
        self.music_message.set_paused(self.paused)
        await self.music_message.update_music_message()
        await interaction.response.defer()

    async def next_callback(self, interaction):
        self.voice_client.stop()
        await interaction.response.defer()

    async def queue_callback(self, interaction):
        if (self.queue_open == False):
            self.queue_open = True
            idx = 1
            content = "```"
            for music in self.queue:
                content += "{}. ".format(idx)
                content += music.title
                content += "\n"
                idx += 1
            content += "```"
            close_btn = discord.ui.Button(label = "Close")
            close_btn.callback = self.queue_close_callback
            view = discord.ui.View(timeout = None)
            view.add_item(close_btn)
            await interaction.response.send_message(content = content, view = view)
            self.queue_message = await interaction.original_response()
        else:
            await interaction.response.defer()

    async def queue_close_callback(self, interaction):
        self.queue_open = False
        await self.queue_message.delete()
        await interaction.response.defer()

    async def connect(self):
        if (self.voice_client == None):
            self.voice_client = await self.channel.connect()
        
    def play(self):
        self.playing = True
        self.music_message.playing = self.playing
        play_music = discord.FFmpegPCMAudio(executable = "ffmpeg", source = self.music)
        self.voice_client.play(play_music, after = self.after)

    def after(self, error):
        if (self.repeat == True):
            self.play()
        else:
            if (len(self.queue) != 0):
                curr_music = self.queue[0]
                if (len(self.queue) > 1):
                    next_music = self.queue[1]
                else:
                    next_music = youtube.Music()
                self.queue.remove(curr_music)
                self.music_message.desc = curr_music.title
                self.music_message.url = "https://www.youtube.com/watch?v={}".format(curr_music.video_id)
                self.music_message.thumbnail = curr_music.thumbnail["url"]
                self.music_message.next_music = next_music.title
                future = asyncio.run_coroutine_threadsafe(self.music_message.update_music_message(), self.loop)
                future.result()
                self.music = curr_music
                self.video_id = curr_music.video_id
                self.download()
                self.play()
            else:
                self.playing = False
                self.music_message.playing = self.playing
                future = asyncio.run_coroutine_threadsafe(self.voice_client.disconnect(), self.loop)
                future.result()
                self.music_message.desc = "No Playing"
                self.music_message.url = ""
                self.music_message.thumbnail = ""
                self.music_message.next_music = ""
                future = asyncio.run_coroutine_threadsafe(self.music_message.update_music_message(), self.loop)
                future.result()

    async def queue_insert(self, music):
        if (len(self.queue) == 0):
            self.music_message.next_music = music.title
            await self.music_message.update_music_message()
        self.queue.append(music)
        #self.playlist.append(music)