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
> First of all, you need Discord server as environment for remote controlling PySilon. In order to do that, create new one.

<img src="https://user-images.githubusercontent.com/44233157/203310675-fc589377-63f7-43f0-b69e-ec7bfaa75b5d.jpg" />





