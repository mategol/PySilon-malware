from filesplit.merge import Merge
from shutil import copy2, rmtree
import os
# end of imports
# on reaction add
elif str(reaction) == '📤':
    #.log Reaction is "confirm upload" 
    if expectation == 'onefile':
        #.log One file gets uploaded 
        split_v1 = str(one_file_attachment_message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        #.log Fetched file to download 
        await one_file_attachment_message.attachments[0].save(fp='/'.join(working_directory) + '/' + filename)
        #.log Downloaded a file 
        async for message in reaction.message.channel.history(limit=2):
            await message.delete()
            #.log Removed the message 
        await reaction.message.channel.send('```Uploaded  ' + filename + '  into  ' + '/'.join(working_directory) + '/' + filename + '```')
        #.log Sent message about success 
        expectation = None
    elif expectation == 'multiplefiles':
        #.log Multiple files are getting uploaded 
        try: os.mkdir('temp')
        except: rmtree('temp'); os.mkdir('temp')
        #.log Prepared a download directory 
        await files_to_merge[0][-1].edit(content='```Uploading file 1 of ' + str(len(files_to_merge[1])) + '```')
        #.log Sent initial message about files downloading 
        for i in range(len(files_to_merge[1])):
            split_v1 = str(files_to_merge[1][i].attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            #.log Fetched file to download 
            await files_to_merge[1][i].attachments[0].save(fp='temp/' + filename)
            #.log Downloaded a file 
            await files_to_merge[0][-1].edit(content='```Uploading file ' + str(i+1) + ' of ' + str(len(files_to_merge[1])) + '```')
            #.log Edited the message about downloading progress 
        await files_to_merge[0][-1].edit(content='```Uploading completed```')
        #.log Edited the messahe about downloading progress to "uploading completed" 
        for i in os.listdir('temp'):
            if i != 'manifest':
                os.rename('temp/' + i, 'temp/' + i[:-8])
                #.log Renamed a file 
        Merge('temp', '/'.join(working_directory), files_to_merge[2]).merge(cleanup=True)
        #.log Merged individual files into original one 
        rmtree('temp')
        #.log Removed temporary directory 
        async for message in client.get_channel(channel_ids['file']).history():
            await message.delete()
            #.log Removed a message 
        await reaction.message.channel.send('```Uploaded  ' + files_to_merge[2] + '  into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '```')
        #.log Sent message about successfull upload 
        files_to_merge = [[], [], []]
        expectation = None
# on message
elif message.content == '.done':
    #.log Message is "done" 
    await message.delete()
    #.log Removed the message 
    if expectation == 'multiplefiles':
        #.log Multiple files were logged 
        files_to_merge[0].append(await message.channel.send('```This files will be uploaded and merged into  ' + '/'.join(working_directory) + '/' + files_to_merge[2] + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```'))
        #.log Sent message about ongoing file downloading and merging 
        await files_to_merge[0][-1].add_reaction('📤')
        #.log Reacted with "confirm upload" 
        await files_to_merge[0][-1].add_reaction('🔴')
        #.log Reacted with "cancel uploading" 
elif message.content[:7] == '.upload':
    #.log Message is "upload" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        if message.content.strip() == '.upload':
            #.log Author issued empty .upload 
            reaction_msg = await message.channel.send('```Syntax: .upload <type> [name]\nTypes:\n    single - upload one file with size less than 25MB\n    multiple - upload multiple files prepared by Splitter with total size greater than 25MB```'); await reaction_msg.add_reaction('🔴')
            #.log Sent message about usage of .upload 
        else:
            if message.content[8:] == 'single':
                #.log Author requested to upload single file 
                expectation = 'onefile'
                await message.channel.send('```Please send here a file to upload.```')
                #.log Sent message letting to send files 
            elif message.content[8:16] == 'multiple' and len(message.content) > 17:
                #.log Author requested to upload multiple files (divided bigger one) 
                expectation = 'multiplefiles'
                files_to_merge[2] = message.content[17:]
                files_to_merge[0].append(await message.channel.send('```Please send here all files (one-by-one) prepared by Splitter and then type  .done```'))
                #.log Sent message about files logging 
            else:
                #.log The syntax of command is wrong 
                reaction_msg = await message.channel.send('```Syntax: .upload multiple <name>```'); await reaction_msg.add_reaction('🔴')
                #.log Sent message about usage of .upload 
    else:
        #.log Message channel is not file-related 
        reaction_msg = await message.channel.send('||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||'); await reaction_msg.add_reaction('🔴')
        #.log Sent message about wrong channel 
# on message end
elif expectation == 'onefile':
    #.log Message is onefile upload candidate 
    split_v1 = str(message.attachments).split('filename=\'')[1]
    filename = str(split_v1).split('\' ')[0]
    #.log Fetched the file name 
    reaction_msg = await message.channel.send('```This file will be uploaded to  ' + '/'.join(working_directory) + '/' + filename + '  after you react with 📤 to this message, or with 🔴 to cancel this operation```')
    #.log Sent confirmation message for upload 
    await reaction_msg.add_reaction('📤')
    #.log Reacted with "confirm upload" 
    await reaction_msg.add_reaction('🔴')
    #.log Reacted with "cancel uploading" 
    one_file_attachment_message = message
elif expectation == 'multiplefiles':
    #.log Message probably contains part of a bigger file 
    files_to_merge[1].append(message)
    #.log Logged a file to download 
