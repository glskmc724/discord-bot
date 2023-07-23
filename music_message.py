from discord.ui import Button, View
from discord import Embed, Color, ButtonStyle, File

class Music_Message:
    channel = None
    desc = "Enter voice channel and input title"
    url = ""
    thumbnail = ""
    color = Color.random()
    playing = False
    requester = ""
    repeat = False
    paused = False
    next_music = ""
    prev_callback = None
    play_callback = None
    paused_callback = None
    next_callback = None
    repeat_callback = None
    queue_callback = None
    def __init__(self, channel = None):
        self.channel = channel

    def get_ox_emoji(self, field):
        if (field == True):
            return "🟢"
        else:
            return "❌"

    def set_requester(self, requester):
        self.requester = requester

    def set_repeat(self, repeat):
        self.repeat = repeat
    
    def set_paused(self, paused):
        self.paused = paused

    def set_parameters(self, requester, repeat, paused):
        self.set_requester(requester)
        self.set_repeat(repeat)
        self.set_paused(paused)
        
    def create_btn(self, label, style, callback = None):
        btn = Button(label = label, style = style)
        btn.callback = callback
        return btn

    def create_embed(self):
        if (self.paused == True):
            title = "Paused"
        else:
            if (self.playing == True):
                title = "Playing"
            else:
                title = "No Playing"
        embed = Embed(title = title, description = self.desc, url = self.url, color = self.color)
        if (self.thumbnail == ""):
            embed.set_image(url = "https://i.postimg.cc/bwcw1t64/default-thumbnail.jpg")
        else:
            embed.set_image(url = self.thumbnail)
        embed.add_field(name = "Request", value = self.requester, inline = True)
        embed.add_field(name = "Repeat", value = self.get_ox_emoji(self.repeat), inline = True)
        embed.add_field(name = "Paused", value = self.get_ox_emoji(self.paused), inline = True)
        embed.add_field(name = "Next Music", value = self.next_music, inline = False)
        return embed

    def create_view(self):
        prev_btn = self.create_btn(label = "⏮️", style = ButtonStyle.gray, callback = self.prev_callback)
        play_btn = self.create_btn(label = "▶️", style = ButtonStyle.gray, callback = self.play_callback)
        paused_btn = self.create_btn(label = "⏸️", style = ButtonStyle.gray, callback = self.paused_callback)
        next_btn = self.create_btn(label = "⏭️", style = ButtonStyle.gray, callback = self.next_callback)
        repeat_btn = self.create_btn(label = "🔁", style = ButtonStyle.gray, callback = self.repeat_callback)
        queue_btn = self.create_btn(label = "🔽", style = ButtonStyle.gray, callback = self.queue_callback)
        if (self.paused == True):
            btn_list = [prev_btn, play_btn, next_btn, repeat_btn, queue_btn]
        else:
            btn_list = [prev_btn, paused_btn, next_btn, repeat_btn, queue_btn]
        view = View(timeout = None)
        for btn in btn_list:
            view.add_item(btn)
        return view
    
    def create_message(self):
        embed = self.create_embed()
        view = self.create_view()
        return embed, view

    async def create_music_message(self):
        embed, view = self.create_message()
        self.message = await self.channel.send(embed = embed, view = view)
    
    async def update_music_message(self):
        embed, view = self.create_message()
        await self.message.edit(embed = embed, view = view)