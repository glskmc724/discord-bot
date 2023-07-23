from discord import SelectOption
from discord.ui import View, Select, Button
import youtube

class Music_Search:
    channel = None
    keyword = ""
    num_result = 5
    select = Select()
    search_done = False
    search_close = False
    searching = False
    def __init__(self, channel = None, keyword = None, num_result = 5):
        self.channel = channel
        self.keyword = keyword
        self.num_result = num_result
    
    def search(self):
        res = youtube.search_api(self.keyword, num_search = self.num_result)
        self.musics = list()
        for item in res["items"]:
            music = youtube.Music()
            music.title = item["snippet"]["title"]
            music.desc = item["snippet"]["description"]
            music.thumbnail = item["snippet"]["thumbnails"]["medium"]
            music.video_id = item["id"]["videoId"]
            self.musics.append(music)
    
    async def select_callback(self, interaction):
        self.search_done = True
        await interaction.response.defer()
        await self.message.delete()

    def create_select(self):
        opts = list()
        idx = 1
        for music in self.musics:
            option = SelectOption(label = music.title, value = idx)
            opts.append(option)
            idx += 1
        self.select.options = opts
        self.select.callback = self.select_callback

    async def close_btn_callback(self, interaction):
        self.search_close = True
        self.search_done = True
        self.searching = False
        await self.message.delete()
        await interaction.response.defer()

    async def create_music_search(self):
        self.searching = True
        self.search_close = False
        self.search_done = False
        content = "```"
        idx = 1
        for music in self.musics:
            content += "{}. {}\n".format(idx, music.title)
            idx += 1
        content += "```"
        self.create_select()
        view = View(timeout = None)
        view.add_item(self.select)
        close_btn = Button(label = "Close")
        close_btn.callback = self.close_btn_callback
        view.add_item(close_btn)
        self.message = await self.channel.send(content = content, view = view)