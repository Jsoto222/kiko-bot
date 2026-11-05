@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Run "Setup Bot.bat" first to install the dependencies.
  pause
  exit /b 1
)
if not exist ".env" (
  echo Missing .env file. Copy .env.example to .env, then enter your NEW bot token.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" bot.py
if errorlevel 1 echo Bot stopped with an error. Review the message above.
pause
