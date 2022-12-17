cd ..
del ha_snitch_pc.exe
venv\Scripts\pyinstaller.exe --onefile --paths=venv\Lib\site-packages main.py
rename dist\main.exe ha_snitch_pc.exe
move dist\ha_snitch_pc.exe .
rmdir /s /q build
rmdir /s /q dist
del main.spec
