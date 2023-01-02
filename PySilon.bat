@echo off
title PySilon
echo Initializing the virtual environment...
python -m venv pysilon
cls
call pysilon\Scripts\activate.bat
pip install pillow
pip install pyinstaller
cls
python builder.py
echo #===============================================================# & echo # Software terminated.                                          # & echo #                                                               # & echo # If you like this project please consider giving me a star     # & echo # to let others know that this is something worth looking into. # & echo #===============================================================# & echo. & echo.
pause
