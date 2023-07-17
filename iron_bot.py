import discord

TOKEN = 'OTIyNDU2ODExMTM3ODAyMjQw.GaFKer.9wqOXmBKO96WH3CrSQ8Hdjx9CkcIcF8_YmAEQg'
CHANNEL_ID = 1130318451249008784

class Client(discord.Client):
    async def on_ready(self):
        self.channel = self.get_channel(CHANNEL_ID)
        await self.channel.send("Hello World")

    async def on_message(self, message):
        if (message.author == self.user):
            return;
        await self.channel.send(message.content)

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
