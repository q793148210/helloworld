@echo off
setlocal
if not exist dist (
    mkdir dist
)

rem build service executable
pyinstaller --onefile --noconsole --distpath dist --workpath build --name WeChatDaemon_Setup win_service.py
if %ERRORLEVEL% NEQ 0 goto :error

rem build configuration gui
pyinstaller --windowed --distpath dist --workpath build --name WeChatDaemon_Config config_gui.py
if %ERRORLEVEL% NEQ 0 goto :error

rem create helper scripts
(
    echo @echo off
    echo WeChatDaemon_Setup.exe install
    echo WeChatDaemon_Setup.exe start
) > dist\install_service.bat

(
    echo @echo off
    echo WeChatDaemon_Setup.exe stop
    echo WeChatDaemon_Setup.exe remove
) > dist\uninstall_service.bat

echo.
echo Build complete. See dist directory.
endlocal
goto :eof

:error
echo Build failed.
endlocal
exit /b 1
