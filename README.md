# Hello World

This repository includes a simple C program and a Python daemon for sending
scheduled messages via Quantum Messaging.

## Files

- `quantum_messaging.py` – library for sending messages.
- `daemon.py` – reads `config.json` and sends messages at the configured times.
- `config_gui.py` – simple GUI for editing the configuration file.
- `win_service.py` – Windows Service wrapper used when packaging on Windows.
- `config.json` – configuration file created on first run if missing.

## Running the daemon
Edit `config.json` to provide your webhook URL, key, and optional proxies. The default schedule sends a message every Monday and Wednesday at 09:00. Start the daemon with:

```bash
python3 daemon.py
```

The daemon reloads configuration on each cycle so edits to `config.json`
take effect automatically.

## Configuration GUI

Run the GUI to update the webhook URL, key, proxies, schedule and message text.
You can also configure whether to mention everyone or a list of specific
contacts when messages are sent:

```bash
python3 config_gui.py
```

For fixed mentions, enter comma-separated mobile numbers in the list field when
selecting "@固定人".

Changes are written to `config.json` which the daemon reads automatically.
Use the **Test** button to send a one-time test message with the current
settings.

## Packaging for Windows

Install `pywin32`, `pyinstaller` and (optionally) Inno Setup if you wish to
create a self-contained installer. Then run `build_all.bat` which builds the
executables and, when Inno Setup is available, produces an installer in the
`dist` directory. If you encounter a `ModuleNotFoundError` for
`win32timezone`, ensure the pywin32 post-install script has been executed:

```bash
python -m pywin32_postinstall -install
```

```bash
pip install pywin32 pyinstaller
build_all.bat
```

The `dist` directory will contain:

- `WeChatDaemon_Setup.exe` – Windows service wrapper
- `WeChatDaemon_Config.exe` – configuration GUI
- `install_service.bat` – registers and starts the service
- `uninstall_service.bat` – stops and removes the service
If Inno Setup was available, you'll also get `WeChatDaemon_Installer.exe` which
copies the files into `C:\Program Files\WeChatDaemon`, installs the service
and creates shortcuts.

Run `install_service.bat` to manually register the daemon or
double‑click the generated installer for a one-step setup. Use
`uninstall_service.bat` or the Windows "Add/Remove Programs" entry to remove it.
