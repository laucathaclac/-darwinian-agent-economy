@echo off
setlocal
cd /d "%~dp0.."
if "%~1"=="" (
  echo Usage: RUN_TASK_WORKER.bat path\to\task.json
  exit /b 2
)
py -3 scripts\dae_task_worker.py --manifest "%~1" --output work-output
endlocal
