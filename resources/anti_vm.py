import psutil
import os

def is_running_in_vm():
    vm_files = [
        "C:\\windows\\system32\\vmGuestLib.dll",
        "C:\\windows\\system32\\vm3dgl.dll",
        "C:\\windows\\system32\\vboxhook.dll",
        "C:\\windows\\system32\\vboxmrxnp.dll",
        "C:\\windows\\system32\\vmsrvc.dll",
        "C:\\windows\\system32\\drivers\\vmsrvc.sys"
    ]
    vm_processes = [ # these are vmware but might add other ones later if I find any
        'vmtoolsd.exe', 
        'vmwaretray.exe', 
        'vmwareuser.exe']

    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in vm_processes:
            return True
    for file_path in vm_files:
        if os.path.exists(file_path):
            return True


    return False
