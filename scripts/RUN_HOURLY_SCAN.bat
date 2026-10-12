@echo off
setlocal
cd /d "%~dp0.."
if not exist reports mkdir reports
py -3 scripts\dae_hourly_scan.py >> reports\hourly.log 2>&1
endlocal
