import discord

client = discord.Client()
bot_token = ''   # Paste here BOT-token

channel_ids = {
    'main': 831567586344697868
}

@client.event 
async def on_ready():  
    await client.get_channel(channel_ids['main']).send('New PC session')

client.run(bot_token)
