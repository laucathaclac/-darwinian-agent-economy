@echo off
setlocal
cd /d "%~dp0.."
if not exist reports mkdir reports
py -3 scripts\dae_hourly_scan.py >> reports\hourly.log 2>&1
if errorlevel 1 (
  echo Scanner failed. See reports\hourly.log
  endlocal
  exit /b 1
)
py -3 scripts\dae_opportunity_advisor.py >> reports\hourly.log 2>&1
if errorlevel 1 (
  echo Advisor failed. See reports\hourly.log
  endlocal
  exit /b 1
)
echo DAE scan and opportunity advice complete.
endlocal
