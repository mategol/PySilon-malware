# Building standalone executable

</span>

### To be able to compile your malware, you need to create Python Virtual Environment:
`python -m venv pysilon`
<br />

### Then, activate it with:
`pysilon\Scripts\activate.bat`
<br />

### If you see "(pysilon)" at the beginning of CMD prompt, it means that so far so good.
### Now, install all requirements with:
`pip install -r requirements.txt`<br />
`pip install pyinstaller`
<br />

### Now, you are ready to run `compiler_obsolete.py`:
`python compiler_obsolete.py`
<br />

### You will be asked how do you want to build the malware:
`[1] - single` -> RAT will be designed for only one target PC<br />
`[2] - multiple` -> RAT will be designed to run on multiple PCs<br />
> If you choose `[1]`, you will be prompted to specify channel-IDs for controlling the malware

> But if you choose `[2]`, you will need to specify only Discord Server ID (+ BOT-token and naming info)

### Then, continue by writing information prompted by the script.
