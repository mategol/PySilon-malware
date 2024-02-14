from pyautogui import hotkey
from time import sleep
# Code
countdown = 10 # Time of Prank Execution Duration
while countdown != 0:
    hotkey("win", "d")
    sleep(1)
    hotkey("win", "d")
    countdown -= 1