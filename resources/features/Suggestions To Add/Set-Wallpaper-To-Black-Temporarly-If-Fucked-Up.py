import ctypes
import os

def set_wallpaper(image_path):
    # Define the path to the image
    image_path = os.path.abspath(image_path)

    # Call the SystemParametersInfo function from user32.dll to set the wallpaper
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)

# Call the function to set the wallpaper (provide the path to the image)
set_wallpaper("Don't-Change.jpg")
