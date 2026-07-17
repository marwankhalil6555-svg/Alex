@echo off
:: Check if the script is already running in a hidden state
if "%~1"=="hidden" goto :run_script

:: Relaunch this batch file using PowerShell with a hidden window
powershell -Command "Start-Process '%~f0' -ArgumentList 'hidden' -WindowStyle Hidden"
exit

:run_script
:: --- Your original logic goes below ---
cd /d D:\Hub\Alex
py -3.12 script.py
exit
