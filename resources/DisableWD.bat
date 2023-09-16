@echo off
set "services=HKLM\SYSTEM\ControlSet001\Services"
::Windows Defender
reg add "%services%\MsSecFlt" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\SecurityHealthService" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\Sense" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\WdBoot" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\WdFilter" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\WdNisDrv" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\WdNisSvc" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\WinDefend" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\wscsvc" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
::WindowsSystemTray
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "SecurityHealth" /f >NUL 2>nul
::System Guard
reg add "%services%\SgrmAgent" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\SgrmBroker" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
::WebThreatDefSvc
reg add "%services%\webthreatdefsvc" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
reg add "%services%\webthreatdefusersvc" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
for /f %%i in ('reg query "%services%" /s /k "webthreatdefusersvc" /f 2^>nul ^| find /i "webthreatdefusersvc" ') do (
  reg add "%%i" /v "Start" /t REG_DWORD /d "4" /f >NUL 2>nul
)
::
::reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\smartscreen.exe" /v "Debugger" /t REG_SZ /d "%%windir%%\System32\taskkill.exe" /f >NUL 2>nul
taskkill /f /im smartscreen.exe >NUL 2>nul
for %%j in (
	"%systemroot%\system32\smartscreen.exe"
) do (
	if not exist "%%j.revi" if exist %%j (
		takeown /F %%j /A >NUL 2>nul
		icacls %%j /grant Administrators:F >NUL 2>nul
		copy "%%j" "%%j.revi" /v >NUL 2>nul
		del "%%j" >NUL 2>nul
	)
)
:: reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Associations" /v "DefaultFileTypeRisk" /t REG_DWORD /d "6152" /f >NUL 2>nul
:: reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Attachments" /v "SaveZoneInformation" /t REG_DWORD /d "1" /f >NUL 2>nul
:: reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Associations" /v "LowRiskFileTypes" /t REG_SZ /d ".avi;.bat;.com;.cmd;.exe;.htm;.html;.lnk;.mpg;.mpeg;.mov;.mp3;.msi;.m3u;.rar;.reg;.txt;.vbs;.wav;.zip;" /f >NUL 2>nul
:: reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Associations" /v "ModRiskFileTypes" /t REG_SZ /d ".bat;.exe;.reg;.vbs;.chm;.msi;.js;.cmd" /f >NUL 2>nul
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v "SmartScreenEnabled" /t REG_SZ /d "Off" /f >NUL 2>nul
reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SmartScreen" /v "ConfigureAppInstallControlEnabled" /t REG_DWORD /d "0" /f >NUL 2>nul
reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SmartScreen" /v "ConfigureAppInstallControl" /t REG_DWORD /d "0" /f >NUL 2>nul
reg add "HKLM\Software\Policies\Microsoft\Windows Defender\SmartScreen" /v "EnableSmartScreen" /t REG_DWORD /d "0" /f >NUL 2>nul
reg add "HKCU\Software\Policies\Microsoft\MicrosoftEdge\PhishingFilter" /v "EnabledV9" /t REG_DWORD /d "0" /f >NUL 2>nul
reg add "HKLM\Software\Policies\Microsoft\MicrosoftEdge\PhishingFilter" /v "EnabledV9" /t REG_DWORD /d "0" /f >NUL 2>nul
::Fixes slow app loading issues on 11+
reg add "HKLM\SYSTEM\ControlSet001\Control\CI\Policy" /v "VerifiedAndReputablePolicyState" /t REG_DWORD /d "1" /f >NUL 2>nul
goto :EOF