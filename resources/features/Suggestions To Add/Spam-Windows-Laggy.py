from pyautogui import hotkey
from time import sleep
# Code
key = True # Active While
infiniteKey = False # Infinite or Finite the Code
repeatKey = 99 # How Much it Is Going to Repeat
while key == True:
    if repeatKey != 0:
        hotkey("win", "e")
        if repeatKey != 0: # Is Finite or Infinite? - is Finite
            repeatKey -= 1
            if infiniteKey == True: # Is Infinite
                repeatKey += 5
        elif infiniteKey == True: # Is Infinite
            repeatKey += 5
    else:
        key == False
        quit()