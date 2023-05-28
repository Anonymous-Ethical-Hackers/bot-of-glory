@echo off
@echo installing files
start pip install discord
start python bot.py
echo python bot.py > start.bat
del install.bat
exit
