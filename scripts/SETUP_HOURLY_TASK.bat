@echo off
setlocal
cd /d "%~dp0.."
set "TASKNAME=DAE-Hourly-Paid-Task-Scan"
set "RUNNER=%~dp0RUN_HOURLY_SCAN.bat"
schtasks /Create /F /SC HOURLY /MO 1 /TN "%TASKNAME%" /TR "cmd.exe /c ""%RUNNER%"""
if errorlevel 1 (
 echo Could not create scheduled task. Try Run as administrator.
 pause
 exit /b 1
)
echo Hourly scan scheduled. To remove: schtasks /Delete /TN "%TASKNAME%" /F
pause
