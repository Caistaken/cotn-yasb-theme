@echo off
py -m pip install PyQt6
xcopy /E /I /Y "%~dp0config" "%USERPROFILE%\.config\yasb"
pause