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
- browse and kill running processes
- execute files
- run CMD commands
- update itself (todo)

# Preparation
This malware is designed for Windows, however, you can prepare everything on Linux as well.<br />
`git clone https://github.com/mategol/pylison-python`<br />
`pip install -r requirements.txt`<br />
<a href="https://github.com/mategol/pysilon-python/edit/main/README.md#setup">`Follow the Setup instructions`</a>

# Available commands
`.ss` - take screenshot at any time<br />
`.join` - join voice-channel and stream live microphone input<br />
`.show <what-to-show>` - get list of running processes or available commands<br />
`.kill <process-ID>` - kill any running process<br />
`.clear` - clear messages from file-related channel<br />
`.pwd` - show working directory (file-related channel only)<br />
`.tree` - show tree of working directory (file-related channel only)<br />
`.ls` - list content of working directory (file-related channel only)<br />
`.cd <dir>` - change working directory (file-related channel only)<br />
`.download <file-or-dir>` - download any file or zipped directory (also greater than 8MB ones) from target PC (file-related channel only)<br />
`.upload <type> [name]` - upload any file or zipped directory (also greater than 8MB ones) onto target PC (file-related channel only)<br />
`.start <file>` - run any file on target PC (file-related channel only)<br />
`.remove <file-or-dir>` - remove file or directory on target PC<br />
`.update` - update PySilon remotely<br />
`.implode <access-code>` - remove PySilon from target PC and clean the "evidence"



















# Setup
<b>This process consists of 3 stages:</b>
> <a href="https://github.com/mategol/pysilon-python/edit/main/README.md#prepare-discord-server-and-discord-bot">1. Prepare Discord server and Discord BOT</a><br />
> <a href="https://github.com/mategol/pysilon-python/edit/main/README.md#set-up-required-values-in-source-code">2. Set up required values in source code</a><br />
> 3. Compile malware to Windows executable<br />
### Prepare Discord server and Discord BOT
> First of all, you need Discord server as environment for remote controlling PySilon. In order to do that, create new one:

<img src="https://user-images.githubusercontent.com/44233157/203310675-fc589377-63f7-43f0-b69e-ec7bfaa75b5d.jpg" />

> Then, create 4 text-channels and 1 voice-channel for different use:<br />
> • main -> for main KeyLogger output and general commands<br />
> • spam-gaming -> for filtered KeyLogger output while target is (for example) playing game<br />
> • recordings -> for storing microphone recordings<br />
> • file-related -> for everything that is related to files<br />
> • Live microphone -> for streaming live microphone input

<img src="https://user-images.githubusercontent.com/44233157/203312123-2d5015a2-6a2e-46fd-8104-f1fc5ff409a9.jpg" />

> Then, go to <a href="https://discord.com/developers/applications">Discord Developer Portal</a> and create new application:

<img src="https://user-images.githubusercontent.com/44233157/203314173-20b1ff5e-c2e4-4fad-995a-63aaa8bd4913.jpg" />

> Then, go to the BOT section and add a BOT:

<img src="https://user-images.githubusercontent.com/44233157/203314786-d171c333-febe-47d3-8670-bd6cf09b98ea.jpg" />

> Then, check all "intents" and save changes:

<img src="https://user-images.githubusercontent.com/44233157/203315507-95ded29a-d6db-4681-9715-c70c27aabd0f.png" />

> Then, reset BOT-Token and copy it for later use:

<img src="https://user-images.githubusercontent.com/44233157/203316364-71fd167d-bf0c-4592-90f3-992da45b6891.jpg" />

> Then, go to "OAuth2" section and "URL Generator" tab:

<img src="https://user-images.githubusercontent.com/44233157/203318137-fe379bb9-e94b-4572-80f4-783f32c2d81f.png" />

> THen, check "bot" scope and "Administrator" permissions:

<img src="https://user-images.githubusercontent.com/44233157/203318332-27c1a692-3e56-41e4-b7df-0f0289768806.png" />

> Then, copy and open generated URL. New window will appear. Select "PySilon controller" server and BOT will join:

<img src="https://user-images.githubusercontent.com/44233157/203319649-e4db527a-741e-4436-8bb1-d7fe674b0e2b.jpg" />

> As you can see, BOT is now in the server:

<img src="https://user-images.githubusercontent.com/44233157/203319836-e7aeb93f-3c22-491b-aea2-cd2aaa41d65d.png" /><br />

### Set up required values in source code

> To make it possible, you need to enable "Developer mode" in Discord settings

<img src="https://user-images.githubusercontent.com/44233157/203321226-e01e4c39-678b-4f77-9bee-1607ad43c1d0.jpg" />

> Now, open "main.py" in any text editor and paste BOT-Token coped earlier in 47th line:

```python
bot_token = ''   # Paste here BOT-token
```

> Now, set program name in 48th line that will be shown in registry:   (something like legitimate software)
```python
software_registry_name = 'PySilon'   # Software name shown in registry
```

> You can also change directory name (49th line) that will be created in `C:/Users/{username}/` and executable name (50th line):
```python
software_directory_name = software_registry_name
software_executable_name = software_registry_name.replace(' ', '') + '.exe'   # MUST end with '.exe'
# As you can see, theese variables are set based on registry name by default. However you can just change it to string if you want
```

> To set channel-IDs in lines 53-57, you need to copy them by right-clicking on channel and then 'Copy ID':

<img src="https://user-images.githubusercontent.com/44233157/203323394-27ff946c-4a9b-4c83-ae77-9dec1fa14842.jpg" />

> `Now, everything is set up for compiling the malware into Windows executable`






