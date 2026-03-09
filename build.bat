@echo off
echo Building Egyptian Ratscrew...
pyinstaller main.spec --distpath dist --workpath build --noconfirm
echo.
echo Done! Run dist\EgyptianRatscrew.exe to play.
pause
