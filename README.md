# PySilon
Advanced RAT malware written in Python, fully controllable through Discord.

# Disclaimer
> Information and code provided on this repository are for educational purposes only. The creator is no way responsible for any direct or indirect damage caused due to the misusage of the information. Everything you do, you are doing at your own risk and responsibility.

# Features
PySilon malware can do plenty of things, like:
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
This malware is designed for Windows, however, you can prepare everything on Linux as well.
```
git clone https://github.com/mategol/pylison-python
pip install -r requirements.txt
```

# Setup
This process consists of 3 stages:
> 1. Prepare Discord server and Discord BOT<br />
> 2. Setup required values in source code<br />
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



