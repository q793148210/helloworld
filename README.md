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

Run the GUI to update the webhook URL, key, proxies, schedule and message text:

```bash
python3 config_gui.py
```

Changes are written to `config.json` which the daemon reads automatically.
Use the **Test** button to send a one-time test message with the current
settings.

## Packaging for Windows

Install `pywin32` and `pyinstaller` and then run `build_all.bat` to create
the service and configuration GUI executables. The script places everything
in a new `dist` directory.

```bash
pip install pywin32 pyinstaller
build_all.bat
```

The `dist` directory will contain:

- `WeChatDaemon_Setup.exe` – Windows service wrapper
- `WeChatDaemon_Config.exe` – configuration GUI
- `install_service.bat` – registers and starts the service
- `uninstall_service.bat` – stops and removes the service

Run `install_service.bat` to install the daemon or `uninstall_service.bat`
to remove it.
