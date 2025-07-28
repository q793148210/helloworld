@echo off

setlocal enabledelayedexpansion

rem === Set working directory to script's location ===
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

rem === Create dist output directory ===

if not exist dist (
    mkdir dist
)

rem === Clean previous build files and PyInstaller configs ===
if exist build (
    rmdir /s /q build
)
if exist __pycache__ (
    rmdir /s /q __pycache__
)
for %%f in (*.spec) do (
    del "%%f"
)

rem === Package service program win_service.py ===
echo.
echo 🔨 Building WeChatDaemon_Setup.exe ...
pyinstaller --onefile --noconsole --distpath dist --workpath build --name WeChatDaemon_Setup --hidden-import=win32timezone win_service.py
if %ERRORLEVEL% NEQ 0 goto :error

rem === Package configuration GUI config_gui.py ===
echo.
echo 🔨 Building WeChatDaemon_Config.exe ...
pyinstaller --windowed --distpath dist --workpath build --name WeChatDaemon_Config config_gui.py
if %ERRORLEVEL% NEQ 0 goto :error

rem === Create service install script install_service.bat ===
echo.
echo 🧪 Creating install_service.bat ...
(
    echo @echo off
    echo cd /d %%~dp0

    echo WeChatDaemon_Setup.exe install
    echo WeChatDaemon_Setup.exe start
) > dist\install_service.bat


rem === Create service uninstall script uninstall_service.bat ===
echo.
echo 🧪 Creating uninstall_service.bat ...
(
    echo @echo off
    echo cd /d %%~dp0

    echo WeChatDaemon_Setup.exe stop
    echo WeChatDaemon_Setup.exe remove
) > dist\uninstall_service.bat

echo.

echo ✅ Build complete! All files are in the dist\ folder.
endlocal
exit /b 0

:error
echo ❌ Build failed with error level %ERRORLEVEL%.
endlocal
exit /b %ERRORLEVEL%

