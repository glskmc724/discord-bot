import discord
import iron_config
import asyncio

import music_message
import music_search
import music_play

search_eng_cmd = "!search"
search_eng_cmd_len = len(search_eng_cmd)
search_kor_cmd = "!검색"
search_kor_cmd_len = len(search_kor_cmd)
loop = None

delete_cmd = "!delete"
class Client(discord.Client):
    music_message = dict()
    music_search = dict()
    music_play = dict()

    def verify_channel(self, ch):
        channels_list = open("channels.list", "r").readlines()
        for channel in channels_list:
            if (channel[0] == '#'):
                continue
            else:
                if (ch == int(channel)):
                    return True
        return False

    async def on_ready(self):
        channels_list = open("channels.list", "r").readlines()
        for channel in channels_list:
            if (channel[0] == '#'):
                continue
            else:
                self.music_search[int(channel)] = music_search.Music_Search(config.youtube_api_key)
                self.music_search[int(channel)].channel = self.get_channel(int(channel))

                self.music_message[int(channel)] = music_message.Music_Message()
                self.music_message[int(channel)].channel = self.get_channel(int(channel))

                self.music_play[int(channel)] = music_play.Music_Play()
                self.music_play[int(channel)].loop = self.loop
                self.music_play[int(channel)].music_message = self.music_message[int(channel)]
                
                await self.get_channel(int(channel)).purge(limit = 1000)

                self.music_message[int(channel)].play_callback = self.music_play[int(channel)].play_callback
                self.music_message[int(channel)].paused_callback = self.music_play[int(channel)].paused_callback
                self.music_message[int(channel)].repeat_callback = self.music_play[int(channel)].repeat_callback
                self.music_message[int(channel)].next_callback = self.music_play[int(channel)].next_callback
                self.music_message[int(channel)].queue_callback = self.music_play[int(channel)].queue_callback
                await self.music_message[int(channel)].create_music_message()

    def is_search_eng_cmd(self, content):
        if (content[:search_eng_cmd_len] == "!search"):
            return content[search_eng_cmd_len + 1:]
        else:
            return False
        
    def is_search_kor_cmd(self, content):
        if (content[:search_kor_cmd_len] == "!검색"):
            return content[search_kor_cmd_len + 1:]
        else:
            return False

    def is_cmd(self, content, cmd):
        if (content[:len(cmd)] == cmd):
            return True
        else:
            return False
    
    async def print_music_message(self, channel_id, music, author):
        voice_client = self.music_play[channel_id].voice_client
        if (voice_client != None):
            if (voice_client.is_playing() == True or voice_client.is_paused() == True):
                await self.music_play[channel_id].queue_insert(music)
                return
        self.music_message[channel_id].desc = music.title
        self.music_message[channel_id].url = "https://www.youtube.com/watch?v={}".format(music.video_id)
        self.music_message[channel_id].thumbnail = music.thumbnail["url"]
        self.music_message[channel_id].set_parameters(requester = author, repeat = False, paused = False)
        await self.music_message[channel_id].update_music_message()

    async def on_message(self, message):
        if (message.author == self.user):
            return
    
        channel_id = message.channel.id

        if (self.verify_channel(channel_id) == False):
            return

        try:
            voice_channel_id = message.author.voice.channel.id
        except:
            await message.delete()
            return
        
        voice_channel = self.get_channel(voice_channel_id)
        content = message.content

        if (self.is_cmd(content, "!delete")):
            await message.channel.purge(limit = 1000)
            return

        keyword = self.is_search_eng_cmd(content) or self.is_search_kor_cmd(content)
        self.music_play[channel_id].channel = voice_channel

        if (keyword != False):
            if (self.music_search[channel_id].searching == True):
                await message.delete()
                return
            self.music_search[channel_id].keyword = keyword
            self.music_search[channel_id].num_result = 5
            self.music_search[channel_id].search()
            await self.music_search[channel_id].create_music_search()
            while (not self.music_search[channel_id].search_done):
                await asyncio.sleep(0.1)
            if (self.music_search[channel_id].search_close == True):
                await message.delete()
                return
            num_select = self.music_search[channel_id].select.values[0]
            music = self.music_search[channel_id].musics[int(num_select) - 1]

            await self.print_music_message(channel_id, music, message.author)
            playing = self.music_play[channel_id].playing

            if (playing != True):
                self.music_play[channel_id].video_id = music.video_id
                self.music_play[channel_id].download()
                await self.music_play[channel_id].connect()
                self.music_play[channel_id].play()
            self.music_search[channel_id].searching = False
        else:
            self.music_search[channel_id].keyword = content
            self.music_search[channel_id].num_result = 1
            self.music_search[channel_id].search()
            music = self.music_search[channel_id].musics[0]

            await self.print_music_message(channel_id, music, message.author)
            playing = self.music_play[channel_id].playing

            if (playing != True):
                self.music_play[channel_id].video_id = music.video_id
                self.music_play[channel_id].download()
                await self.music_play[channel_id].connect()
                self.music_play[channel_id].play()
        
        await message.delete()
      

if (__name__ == "__main__"):
    intents = discord.Intents.default()
    intents.message_content = True
    config = iron_config.Config()
    client = Client(intents = intents)
    client.run(config.discord["discord_bot_token"])
