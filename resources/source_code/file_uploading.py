from filesplit.merge import Merge
from shutil import copy2, rmtree
import os
# end of imports

# on reaction add
elif str(reaction) == '📤':
    if expectation == 'onefile':
        split_v1 = str(one_file_attachment_message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        await one_file_attachment_message.attachments[0].save(fp='/'.join(working_directory) + '/' + filename)
        async for message in reaction.message.channel.history(limit=2):
            await message.delete()
        await reaction.message.channel.send('```Uploaded  ' + filename + '  into  ' + '/'.join(working_directory) + '/' + filename + '```')
        expectation = None

    elif expectation == 'multiplefiles':
        try: os.mkdir('temp')
        except: rmtree('temp'); os.mkdir('temp')

        await files_to_merge[0][-1].edit(content='```Uploading file 1 of ' + str(len(files_to_merge[1])) + '```')
        for i in range(len(files_to_merge[1])):
            split_v1 = str(files_to_merge[1][i].attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            await files_to_merge[1][i].attachments[0].save(fp='temp/' + filename)
            await files_to_merge[0][-1].edit(content='```Uploading file ' + str(i+1) + ' of ' + str(len(files_to_merge[1])) + '```')
        await files_to_merge[0][-1].edit(content='```Uploading completed```')
        for i in os.listdir('temp'):
            if i != 'manifest':
                os.rename('temp/' + i, 'temp/' + i[:-8])
        Merge('temp', '/'.join(working_directory), files_to_merge[2]).merge(cleanup=True)
        rmtree('temp')
        async for message in client.get_channel(channel_ids['file']).history():
            await message.delete()
        await reaction.message.channel.send('```Uploaded  ' + files_to_merge[2] + '  into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '```')
        files_to_merge = [[], [], []]
        expectation = None

# on message
elif message.content == '.done':
    await message.delete()
    if expectation == 'multiplefiles':
        files_to_merge[0].append(await message.channel.send('```This files will be uploaded and merged into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```'))
        await files_to_merge[0][-1].add_reaction('📤')
        await files_to_merge[0][-1].add_reaction('🔴')

elif message.content[:7] == '.upload':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content.strip() == '.upload':
            reaction_msg = await message.channel.send('```Syntax: .upload <type> [name]\nTypes:\n    single - upload one file with size less than 8MB\n    multiple - upload multiple files prepared by Splitter with total size greater than 8MB```'); await reaction_msg.add_reaction('🔴')
        else:
            if message.content[8:] == 'single':
                expectation = 'onefile'
                await message.channel.send('```Please send here a file to upload.```')
            elif message.content[8:16] == 'multiple' and len(message.content) > 17:
                expectation = 'multiplefiles'
                files_to_merge[2] = message.content[17:]
                files_to_merge[0].append(await message.channel.send('```Please send here all files (one-by-one) prepared by Splitter and then type  .done```'))
            else: reaction_msg = await message.channel.send('```Syntax: .upload multiple <name>```'); await reaction_msg.add_reaction('🔴')
    else:
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')

# on message end
elif expectation == 'onefile':
    split_v1 = str(message.attachments).split('filename=\'')[1]
    filename = str(split_v1).split('\' ')[0]
    reaction_msg = await message.channel.send('```This file will be uploaded to  ' + '/'.join(working_directory) + '/' + filename + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```')
    await reaction_msg.add_reaction('📤')
    await reaction_msg.add_reaction('🔴')
    one_file_attachment_message = message

elif expectation == 'multiplefiles':
    files_to_merge[1].append(message)
