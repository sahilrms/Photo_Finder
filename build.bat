@echo off
setlocal

:: Create icon if it doesn't exist
if not exist app_icon.ico (
    echo Creating icon...
    python create_icon.py
)

:: Build the executable
echo Building executable...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon=app_icon.ico ^
    --add-data "C:/Python311/Lib/site-packages/cv2;cv2" ^
    --hidden-import=opencv_python ^
    --hidden-import=PIL ^
    --name "Photo_Finder" ^
    photo_finder.py

echo.
echo Build complete! The executable is in the 'dist' folder.
pause
