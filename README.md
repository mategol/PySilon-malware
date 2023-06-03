<span align='center'>

# `PySilon-rs` 

<span align='left'>

It connects to Discord, making it easy to connect to the host computer.

As of now, there's no GUI yet for it to be built, yet soon to be made.

These are the currently implemented commands:

`.ss` - Take a screenshot and send it.

`.grab <action>` - You can either use "passwords", "wifi" or "discord" in the action argument, it will send it to you.

`.webcam <action>` - You can use "photo" in the action argument, to take a photo of the host's webcam.

`.show <action> [options]` - You can use "processes" in the action argument, this can accept an options argument, which is to select the sorting option, by default it's "name", you can choose "cpu", "mem" or "pid", you can also use "system" to show the system information, or "network" to show the network information, or "components" to show the connected components information, or "disks" to show the connected disks information, or "cpus" to show all the CPU's information.

`.kill <pid>` - Kill a process in the host machine, with the Process ID (PID)

* `.pwd` - Show current working directory.

* `.tree` - Show file tree of the current working directory.

`.proxy <proxy/list/every_file>` - Proxy files greater than 25 MiB (as in proxy, you can choose "gofile", "pixeldrain" or "anonfiles" for now), "list" to list the current proxies, "every_file" to toggle if every file will get proxied, but it may upload slower (or faster).

* `.ls` - Show the working directory files and folders with no recursion.

* `.cd <dir>` - Go to a specificed directory (if it exists)

* `.download <file/dir>` - Download a file or directory (if it's a directory, it will download recursively, meaning it won't pack it in 1 file.)

* `.download_tar <dir>` - Download a directory packed in a tar file.

* `.execute <file>` - Execute a file in the host's PC.

`.cmd <command>` - Run a CMD command in the host's PC.

* `.remove <file/dir>` - Remove a file or directory from the host's PC.

* `.upload <attachment/proxy_url>` - Upload a file into the host's PC.

* `.implode <pysilon_key>` - Remove the RAT from the host's PC without leaving any trace, this is not reversable.

* `.update <pysilon_key> <new_file>` - Update the RAT of the host's PC without having the user on the host's PC to do anything.

`.bsod` - Trigger a BSOD on the host's PC.

* <-- This means that will only work on the file-related channel.

It's also relatively lightweight!
When compiling on release mode, it heights ~16 MiB.