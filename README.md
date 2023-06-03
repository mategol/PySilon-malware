<span align='center'>

# `PySilon`

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/205148071-ed0f810e-be71-4b18-8c6b-94e838ebda5d.png" width=500 /></p>

`Advanced RAT malware written in Python, fully controllable through Discord with dedicated GUI builder to make preparation easier.`
  
</span>

# Table of contents

- <a href="https://github.com/mategol/PySilon-malware#disclaimer">Disclaimer</a>
- <a href="https://github.com/mategol/PySilon-malware#features">Features</a>
- <a href="https://github.com/mategol/PySilon-malware#preparation">Preparation</a>
- <a href="https://github.com/mategol/PySilon-malware#available-commands">Available commands</a>
- <a href="https://github.com/mategol/PySilon-malware#setup">Setup</a>
- <a href="https://github.com/mategol/PySilon-malware#building-standalone-executable">Building executable</a>
- <a href="https://github.com/mategol/PySilon-malware#autonomic-features">Autonomic features</a>
- <a href="https://github.com/mategol/PySilon-malware#commands-manual">Commands manual</a>

# Disclaimer
>
> Information and code provided on this repository are for educational purposes only. The creator is no way responsible for any direct or indirect damage caused due to the misusage of the information. Everything you do, you are doing at your own risk and responsibility.

# Features

### PySilon malware can do plenty of things, like:

- handle multiple PCs (not only one, like in most of the cases)
- possibility to use multiple Discord-BOT Tokens (for emergency situations like Discord banning one Token)
- log every key pressed on keyboard
- take screenshots anytime you want
- take images from webcam
- steal saved WiFi passwords
- record microphone input (24/7) and save it in .wav files
- stream live microphone input on voice channel
- browse files on target PC
- upload and download files from target PC
- grab history, cookies and passwords saved in web browsers
- grab discord tokens and system information
- browse and kill running processes
- execute files
- run CMD commands
- update itself (ToDo)

# Preparation

This malware is designed for Windows and because of some pip packages are available only on Windows (might be changed in future for Linux support), I'm afraid that you can't compile it on Linux (at least with compiler.py):<br />

### Automated, GUI way

`git clone https://github.com/mategol/pysilon-malware`<br />
<a href="https://github.com/mategol/pysilon-malware#setup">`Create Discord BOT and server`</a><br />
`Run the PySilon.bat either using CMD or double clicking on it`<br />

### Manual way (obsolete)

`git clone https://github.com/mategol/pysilon-malware`<br />
<a href="https://github.com/mategol/pysilon-malware#setup">`Create Discord BOT and server`</a><br />
<a href="https://github.com/mategol/PySilon-malware/blob/main/resources/resobuilding_executable_obsolete.md#building-standalone-executable">`Create Virtual Environment (important) - tutorial below`</a><br />
<a href="https://github.com/mategol/PySilon-malware/blob/main/resources/resobuilding_executable_obsolete.md#building-standalone-executable">`Install all requirements`</a><br />
`Run compiler_obsolete.py`<br />

# Available commands

- [.ss](https://github.com/mategol/pysilon-malware#ss) - take screenshot at any time
- [.join](https://github.com/mategol/pysilon-malware#join) - join voice-channel and stream live microphone input
- [.show [what-to-show]](https://github.com/mategol/pysilon-malware#show-what-to-show) - get list of running processes or available commands
- [.kill [process-id]](https://github.com/mategol/pysilon-malware#kill-process-id) - kill any running process
- [.grab [what-to-grab]](https://github.com/mategol/pysilon-malware#grab-what-to-grab) - grab for example saved passwords in web browsers
- [.clear](https://github.com/mategol/pysilon-malware#clear) - clear messages from file-related channel
- [.pwd](https://github.com/mategol/pysilon-malware#pwd) - show working directory
- [.tree](https://github.com/mategol/pysilon-malware#tree) - show tree of working directory
- [.ls](https://github.com/mategol/pysilon-malware#ls) - list content of working directory
- [.cd [dir]](https://github.com/mategol/pysilon-malware#cd-directory) - change working directory
- [.download [file-or-dir]](https://github.com/mategol/pysilon-malware#download-file-or-directory) - download any file or zipped directory (also greater than 8MB ones) from target PC
- [.upload [type] [name]](https://github.com/mategol/pysilon-malware#upload-type-filename) - upload any file or zipped directory (also greater than 8MB ones) onto target PC
- [.execute [file]](https://github.com/mategol/pysilon-malware#execute-file) - run any file on target PC
- [.remove [file-or-dir]](https://github.com/mategol/pysilon-malware#remove-file-or-dir) - remove file or directory on target PC
- [.update](https://github.com/mategol/pysilon-malware#update) - update PySilon remotely
 - [.implode](https://github.com/mategol/pysilon-malware#implode) - remove PySilon from target PC and clean the "evidence"
 command available on file-related channel only


# Setup

### Creating a Discord Server for controlling the malware

<span align='center'>

> First of all, you need Discord server as environment for remote controlling PySilon. In order to do that, create new one:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203310675-fc589377-63f7-43f0-b69e-ec7bfaa75b5d.jpg" /></p>

> Then, go to <a href="https://discord.com/developers/applications">Discord Developer Portal</a> and create new application:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203314173-20b1ff5e-c2e4-4fad-995a-63aaa8bd4913.jpg" /></p>

> Then, go to the BOT section and add a BOT:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203314786-d171c333-febe-47d3-8670-bd6cf09b98ea.jpg" /></p>

> Then, check all "intents" and save changes:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203315507-95ded29a-d6db-4681-9715-c70c27aabd0f.png" /></p>

> Then, reset BOT-Token and copy it for later use:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203316364-71fd167d-bf0c-4592-90f3-992da45b6891.jpg" /></p>

> Then, go to "OAuth2" section and "URL Generator" tab:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203318137-fe379bb9-e94b-4572-80f4-783f32c2d81f.png" /></p>

> Then, check "bot" scope and "Administrator" permissions:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203318332-27c1a692-3e56-41e4-b7df-0f0289768806.png" /></p>

> Then, copy and open generated URL. New window will appear. Select "PySilon controller" server and BOT will join:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319649-e4db527a-741e-4436-8bb1-d7fe674b0e2b.jpg" /></p>

> As you can see, BOT is now on the server:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319836-e7aeb93f-3c22-491b-aea2-cd2aaa41d65d.png" /><br /></p>

> You need to enable "Developer mode" in Discord settings:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203321226-e01e4c39-678b-4f77-9bee-1607ad43c1d0.jpg" /></p>

</span>

<span align='left'>

### Continuation

> Right-click on controller Server and click "Copy ID" (save for later use)

<br />

# Building standalone executable

### Run `PySilon.bat` and GUI will appear. Fill the needed information and click on `Generate source`, then `Compile`

<p align="center"><img src="https://user-images.githubusercontent.com/44233157/210283583-8eed0cdf-0bbe-453c-af16-695d48f6743d.png" /></p><br />

Inside builder, you can `Load configuration` to save time between testing or you can `Load custom...` configuration from desired configuration-file, additionally, you can `Reset` the settings or `Save` them for later. When you `Generate source`, configuration will be automatically saved.

### If you somehow cannot use GUI, you <a href="https://github.com/mategol/PySilon-malware/blob/main/resources/resobuilding_executable_obsolete.md#building-standalone-executable">must use the obsolete way</a> or wait for me to publish the CLI update of builder.
  
<br />

### Multiple Discord BOT tokens

**You can add more than one BOT-token to malware in case of the first one getting banned by Discord (`Emergency token 1/2`). If first token gets banned, PySilon will automatically run with another one (if you set them in compiler.py)**

<br />

`If you encounter any errors, please `<a href='https://github.com/mategol/PySilon-malware/issues/new/choose'>`raise an Issue`</a>` and I will be happy to help as soon as possible.`
<br />

> **`Now, everything is ready for a showtime`**

<br /><br />

# Autonomic features

### `If you react with 📌 to the message, it gets pinned to that channel`
### `If you react with 🔴 to the message, it gets deleted`
### `If victim presses @ key, malware takes screenshot and sends it on #main channel`
### `If victim presses Print_Screen key, malware also takes a screenshot`
### `Reactions (for example ✅📤💀) are used to confirm actions such as killing processes`
### `If you choose 'multi-target' in compiler.py, all channels will be automatically created under category named with Hardware-ID (of PC that malware is running on) once the built executable runs for the first time on a new PC`

<br /><br />

# Commands manual

<br />

### `.ss`
>
> **This command takes a screenshot of target PC at any time:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397679-78bf53de-0a66-4ee2-811e-5b8cf10377dc.png" /></p>

<br />

### `.join`
>
> **This command makes BOT join voice-channel and stream live microphone input:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397968-79001712-5fd1-43cd-a898-774c57c0c1e6.png" /></p>

<br />

### `.show <what-to-show>`
>
> **`<what-to-show>` - as typed, specifies the information that you want to obtain. These can be "`processes`" or "`commands`" at the moment *(without quotes)*.**<br />
> **"`processes`" gives you a list of currently running processes on target PC.**<br />
> **"`commands`" gives you a list of all available commands along with short brief about them.**<br />
> **This command shows you specific types of information:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203438468-43aed4e3-8d21-41a9-87a0-3630b58979b8.jpg" /></p>

<br />

### `.kill <process-id>`
>
> **`<process-id>` - index of process attached after `.show processes` command**<br />
> **This command kills running process:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203439640-f7754516-be78-4e06-81f8-b22f08eeebd1.jpg" /></p>

<br />

### `.grab <what-to-grab>`
>
> **`<what-to-grab>` - as typed, specifies the things you want to grab. These can be "`passwords`" or "`discord`" at the moment *(without quotes)*.**<br />
> **"`passwords`" grabs all passwords saved in web browsers.**<br />
> **"`discord`" grabs Discord authentication Tokens.**<br />
> **"`history`" grabs web browsers history.**<br />
> **"`cookies`" grabs cookies.**<br />
> **This command grabs sensitive data *(for example saved credentials)*:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/205966715-a753397c-df0c-4515-bc88-f44513e5b1e0.png" /></p>

<br />

### `.clear`
>
> **This command clears messages from file-related channel:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203398296-c73b79e8-9f70-45ec-9607-586cd54767a6.png" /></p>

<br />

### `.pwd`
>
> **This command shows you working directory path:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204939055-3bc4da31-b72e-4eea-a153-7b5d712e40ff.png" /></p>

<br />

### `.tree`
>
> **This command shows you file-and-directory structure of working directory:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204939884-a44fb244-f837-4018-b64e-a12ebde2bbcb.jpg" /></p>

<br />

### `.ls`
>
> **This command shows you content of working directory:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204940025-5d1f145f-ebf3-463c-b5f0-48099897fbda.png" /></p>

<br />

### `.cd <directory>`
>
> **This command changes working directory:**<br />

<br />

### `.download <file-or-directory>`
>
> **This command allows you to download a file or zipped directory from target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204940123-454bd16b-bcfd-460f-98bd-0455e0fae984.png" /></p>

<br />

### `.upload <type> [filename]`
>
> **`<type>` - "`single`" or "`multiple`" *(without quotes)***<br />
> **"`single`" means that you want to upload one file *(with size smaller than 8MB)***<br />
> **"`multiple`" means that you want to upload multiple files *(prepared by tools/splitter.py with total size greater than 8MB)***<br />
> **`[filename]` - name of uploaded file *(this option is required only wtih `type` of `multiple`)***<br />
> **This command allows you to upload a file or zipped directory onto target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204941488-ba19a2b7-98aa-42fb-a70f-fd26fb93c2dc.jpg" /></p>

<br />

### `.execute <file>`
>
> **This command starts any file on target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204941945-33ddcf04-9825-400b-8111-8c1540c0208a.jpg" /></p>

<br />

### `.remove <file-or-dir>`
>
> **This command removes any file or directory on target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204947262-7aca6073-2f2e-4af8-b96b-171a52738da0.png" /></p>

<br />

### `.update`
>
> **This command updates already working malware remotely *(with executable prepared by you and splitted by splitter.py)*:**<br />

<br />

### `.implode`
>
> **This command completely removes PySilon malware from target PC and cleans possible evidence. It requires a key generated with tools/compiler.py at <a href="https://github.com/mategol/pysilon-malware#run-toolscompilerpy-and-enter-all-needed-values-to-successfully-build-rat-windows-executable">this step</a>:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204947559-2960d3a6-d259-4592-8b32-7e5193c4cae7.jpg" /></p>

<br />

</span></p>

# ToDo

List of features that should appear in following releases:

- [ ] optional ransomware
- [ ] fork bomb (wabbit)
- [ ] webhook connection in case of unexpected circumstances (like BOT-Token banned by Discord)
- [ ] different acting on Virtual-Machines (like Blue Screen of Death)
- [ ] overall system info grabber with cool Discord Embeds
- [ ] traditional reverse shell creator
- [ ] grab credit cards information
- [ ] optional crypto mining (for example, when victim is idle)
- [ ] grab sessions from popular applications (Steam/Minecraft/Metamask/Exodus/Roblox)
- [ ] replace BTC copied address by your one
- [ ] optimize the code to consume less resources/memory

