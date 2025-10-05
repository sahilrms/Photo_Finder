@echo off
setlocal

:: Create icon if it doesn't exist
if not exist app_icon.ico (
    echo Creating icon...
    python create_icon.py
)

:: Clean up old builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist Photo_Finder.exe del /f /q Photo_Finder.exe

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

:: Copy executable to root
echo Copying executable to root directory...
if exist dist\Photo_Finder.exe (
    copy /y dist\Photo_Finder.exe .
    echo.
    echo Build complete! The executable is ready: Photo_Finder.exe
) else (
    echo Error: Build failed. Check for errors above.
)

pause
