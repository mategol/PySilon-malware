from pyautogui import write, hotkey
from time import sleep
times = 100000000000 # How Much Times it Will Write?
while times != 0:
    hotkey("alt", "tab")
    write("You Have Been Hacked!")
    sleep(0.01)
    hotkey("shift", "enter")