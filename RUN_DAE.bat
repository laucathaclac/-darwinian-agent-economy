@echo off
setlocal
cd /d "%~dp0"
title Darwinian Agent Economy
echo ==========================================
echo DAE - Read-only Opportunity Research
echo ==========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher "py" not found. Install Python 3.11+ and enable PATH.
  goto :fail
)
py -3 --version
if errorlevel 1 goto :fail
if not exist reports mkdir reports
echo.
echo [1/3] Scanning public GitHub Issues...
py -3 scripts\dae_hourly_scan.py
if errorlevel 1 (
  echo Scanner failed or source unavailable. Check the message above.
  goto :fail
)
echo.
echo [2/3] Building opportunity advice...
py -3 scripts\dae_opportunity_advisor.py
if errorlevel 1 goto :fail
echo.
echo [3/3] Generating X / Binance Square search links...
py -3 scripts\dae_external_source_discovery.py
if errorlevel 1 goto :fail
echo.
echo DAE run complete. Funding is not independently verified.
echo Open reports\hourly_opportunity_brief.md and reports\external_source_searches.md
goto :end
:fail
echo.
echo DAE did not complete successfully. Do not treat partial reports as complete.
:end
echo.
pause
endlocal
