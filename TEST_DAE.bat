@echo off
setlocal
cd /d "%~dp0"
title DAE Test Suite
echo Running DAE test suite...
py -3 -m compileall -q src scripts tests
if errorlevel 1 goto :fail
py -3 -m unittest discover -s tests -v
if errorlevel 1 goto :fail
py -3 -m dae.cli demo
if errorlevel 1 goto :fail
echo.
echo ALL LOCAL CHECKS PASSED
goto :end
:fail
echo.
echo CHECKS FAILED - copy the complete CMD output for diagnosis.
:end
echo.
pause
endlocal
