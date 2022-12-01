# PySilon
Advanced RAT malware written in Python, fully controllable through Discord.

# Disclaimer
> Information and code provided on this repository are for educational purposes only. The creator is no way responsible for any direct or indirect damage caused due to the misusage of the information. Everything you do, you are doing at your own risk and responsibility.

# Features
### PySilon malware can do plenty of things, like:
- log every key pressed on keyboard
- take screenshots anytime you want
- record microphone input (24/7) and save it in .wav files
- stream live microphone input on voice channel
- browse files on target PC
- upload and download files from target PC
- grab history, cookies and passwords saved in web browsers
- grab discord tokens and system information
- browse and kill running processes
- execute files
- run CMD commands
- update itself (todo)

# Preparation
This malware is designed for Windows, however, you can prepare everything on Linux as well.<br />
`git clone https://github.com/mategol/pysilon-malware`<br />
`pip install -r requirements.txt`<br />
<a href="https://github.com/mategol/pysilon-malware#setup">`Follow the Setup instructions`</a>

# Available commands
  <a href="https://github.com/mategol/pysilon-malware#ss">`.ss`</a> - take screenshot at any time<br />
  <a href="https://github.com/mategol/pysilon-malware#join">`.join`</a> - join voice-channel and stream live microphone input<br />
  <a href="https://github.com/mategol/pysilon-malware#show-what-to-show">`.show <what-to-show>`</a> - get list of running processes or available commands<br />
  <a href="https://github.com/mategol/pysilon-malware#kill-process-id">`.kill <process-id>`</a> - kill any running process<br />
  <a href="https://github.com/mategol/pysilon-malware#grab-what-to-grab">`.grab <what-to-grab>`</a> - grab for example saved passwords in web browsers<br />
\* <a href="https://github.com/mategol/pysilon-malware#clear">`.clear`</a> - clear messages from file-related channel<br />
\* <a href="https://github.com/mategol/pysilon-malware#pwd">`.pwd`</a> - show working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#tree">`.tree`</a> - show tree of working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#ls">`.ls`</a> - list content of working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#cd-directory">`.cd <dir>`</a> - change working directory<br />
\* <a href="https://github.com/mategol/pysilon-malware#download-file-or-directory">`.download <file-or-dir>`</a> - download any file or zipped directory (also greater than 8MB ones) from target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#upload-type-filename">`.upload <type> [name]`</a> - upload any file or zipped directory (also greater than 8MB ones) onto target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#execute-file">`.execute <file>`</a> - run any file on target PC<br />
\* <a href="https://github.com/mategol/pysilon-malware#remove-file-or-dir">`.remove <file-or-dir>`</a> - remove file or directory on target PC<br />
  <a href="https://github.com/mategol/pysilon-malware#update">`.update`</a> - update PySilon remotely<br />
  <a href="https://github.com/mategol/pysilon-malware#implode">`.implode`</a> - remove PySilon from target PC and clean the "evidence"<br />

<br />\* command available on file-related channel only

# Setup

<b>This process consists of 2 stages:</b>
> <a href="https://github.com/mategol/pysilon-malware#prepare-discord-server-and-discord-bot">1. Prepare Discord server and Discord BOT</a><br />
> <a href="https://github.com/mategol/pysilon-malware#run-toolscompilerpy-and-enter-all-needed-values-to-successfully-build-rat-windows-executable">2. Compile malware to Windows executable</a><br />

<span align='center'>

### Prepare Discord server and Discord BOT

> First of all, you need Discord server as environment for remote controlling PySilon. In order to do that, create new one:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203310675-fc589377-63f7-43f0-b69e-ec7bfaa75b5d.jpg" /></p>

> Then, create 4 text-channels and 1 voice-channel for different use:<br />
> • main -> for main KeyLogger output and general commands<br />
> • spam-gaming -> for filtered KeyLogger output while target is (for example) playing game<br />
> • recordings -> for storing microphone recordings<br />
> • file-related -> for everything that is related to files<br />
> • Live microphone -> for streaming live microphone input

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203312123-2d5015a2-6a2e-46fd-8104-f1fc5ff409a9.jpg" /></p>

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

> THen, check "bot" scope and "Administrator" permissions:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203318332-27c1a692-3e56-41e4-b7df-0f0289768806.png" /></p>

> Then, copy and open generated URL. New window will appear. Select "PySilon controller" server and BOT will join:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319649-e4db527a-741e-4436-8bb1-d7fe674b0e2b.jpg" /></p>

> As you can see, BOT is now in the server:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203319836-e7aeb93f-3c22-491b-aea2-cd2aaa41d65d.png" /><br /></p>

### Get channel IDs for proper messaging

> You need to enable "Developer mode" in Discord settings:

<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203321226-e01e4c39-678b-4f77-9bee-1607ad43c1d0.jpg" /></p>

<br />
  
> To copy channel ID, just right-click on channel and click "Copy ID".
  
<br />

### `Run tools/compiler.py and enter all needed values to successfully build RAT Windows executable.`

<br />

<span align='center'>

> **`Now, everything is set up for compiling the malware into Windows executable`**

<br />

# Commands manual

<br />

### `.ss`
> **This command takes a screenshot of target PC at any time:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397679-78bf53de-0a66-4ee2-811e-5b8cf10377dc.png" /></p>

<br />

### `.join`
> **This command makes BOT join voice-channel and stream live microphone input:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203397968-79001712-5fd1-43cd-a898-774c57c0c1e6.png" /></p>

<br />

### `.show <what-to-show>`
> **`<what-to-show>` - as typed, specifies the information that you want to obtain. These can be "`processes`" or "`commands`" at the moment *(without quotes)*.**<br />
> **"`processes`" gives you a list of currently running processes on target PC.**<br />
> **"`commands`" gives you a list of all available commands along with short brief about them.**<br />
> **This command shows you specific types of information:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203438468-43aed4e3-8d21-41a9-87a0-3630b58979b8.jpg" /></p>

<br />

### `.kill <process-id>`
> **`<process-id>` - index of process attached after `.show processes` command**<br />
> **This command kills running process:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203439640-f7754516-be78-4e06-81f8-b22f08eeebd1.jpg" /></p>

<br />

### `.grab <what-to-grab>`
> **`<what-to-grab>` - as typed, specifies the things you want to grab. These can be "`passwords`" or "`discord`" at the moment *(without quotes)*.**<br />
> **"`passwords`" grabs all passwords saved in web browsers.**<br />
> **"`discord`" grabs Discord authentication Tokens.**<br />
> **"`history`" grabs web browsers history.**<br />
> **"`cookies`" grabs cookies.**<br />
> **This command grabs sensitive data *(for example saved credentials)*:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203449847-57b7c9f4-de62-4b5c-acd6-898b5f8f1520.png" /></p>

<br />

### `.clear`
> **This command clears messages from file-related channel:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/203398296-c73b79e8-9f70-45ec-9607-586cd54767a6.png" /></p>

<br />

### `.pwd`
> **This command shows you working directory path:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204939055-3bc4da31-b72e-4eea-a153-7b5d712e40ff.png" /></p>

<br />

### `.tree`
> **This command shows you file-and-directory structure of working directory:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204939884-a44fb244-f837-4018-b64e-a12ebde2bbcb.jpg" /></p>

<br />

### `.ls`
> **This command shows you content of working directory:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204940025-5d1f145f-ebf3-463c-b5f0-48099897fbda.png" /></p>

<br />

### `.cd <directory>`
> **This command changes working directory:**<br />

<br />

### `.download <file-or-directory>`
> **This command allows you to download a file or zipped directory from target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204940123-454bd16b-bcfd-460f-98bd-0455e0fae984.png" /></p>

<br />

### `.upload <type> [filename]`
> **`<type>` - "`single`" or "`multiple`" *(without quotes)***<br />
> **"`single`" means that you want to upload one file *(with size smaller than 8MB)***<br />
> **"`multiple`" means that you want to upload multiple files *(prepared by tools/splitter.py with total size greater than 8MB)***<br />
> **`[filename]` - name of uploaded file *(this option is required only wtih `type` of `multiple`)***<br />
> **This command allows you to upload a file or zipped directory onto target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204941488-ba19a2b7-98aa-42fb-a70f-fd26fb93c2dc.jpg" /></p>

<br />

### `.execute <file>`
> **This command starts any file on target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204941945-33ddcf04-9825-400b-8111-8c1540c0208a.jpg" /></p>

<br />

### `.remove <file-or-dir>`
> **This command removes any file or directory on target PC:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204947262-7aca6073-2f2e-4af8-b96b-171a52738da0.png" /></p>

<br />

### `.update`
> **This command updates already working malware remotely *(with executable prepared by you and splitted by splitter.py)*:**<br />

<br />

### `.implode`
> **This command completely removes PySilon malware from target PC and cleans possible evidence. It requires a key generated with tools/compiler.py at <a href="https://github.com/mategol/pysilon-malware#run-toolscompilerpy-and-enter-all-needed-values-to-successfully-build-rat-windows-executable">this step</a>:**<br />
<p align='center'><img src="https://user-images.githubusercontent.com/44233157/204947559-2960d3a6-d259-4592-8b32-7e5193c4cae7.jpg" /></p>

<br />

</span>
