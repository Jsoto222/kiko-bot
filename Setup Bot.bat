@echo off
setlocal
cd /d "%~dp0"
echo Setting up Kiko Discord Bot...
py -m venv .venv
if errorlevel 1 (
  echo Could not create the Python environment. Verify Python using: py --version
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :error
echo.
echo Setup complete. Copy .env.example to .env and enter your NEW bot token.
pause
exit /b 0
:error
echo.
echo Setup failed. Read the error above.
pause
exit /b 1
