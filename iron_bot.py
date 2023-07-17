import discord

TOKEN = 'OTIyNDU2ODExMTM3ODAyMjQw.GaFKer.9wqOXmBKO96WH3CrSQ8Hdjx9CkcIcF8_YmAEQg'
CHANNEL_ID = 1130318451249008784

class Client(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(CHANNEL_ID)
        await channel.send("Hello World")

intents = discord.Intents.default()
intents.message_content = True
client = Client(intents=intents)
client.run(TOKEN)
