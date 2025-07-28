# Hello World

This repository includes a simple C program and a Python daemon for sending
scheduled messages via Quantum Messaging.

## Files

- `hello.c` – example C source.
- `quantum_messaging.py` – library for sending messages.
- `daemon.py` – reads `config.json` and sends messages at the configured times.
- `config_gui.py` – simple GUI for editing the configuration file.
- `win_service.py` – Windows Service wrapper used when packaging on Windows.
- `config.json` – configuration file created on first run if missing.

## Running the daemon

Edit `config.json` to provide your webhook URL and key. The default schedule
sends a message every Monday and Wednesday at 09:00. Start the daemon with:

```bash
python3 daemon.py
```

The daemon reloads configuration on each cycle so edits to `config.json`
take effect automatically.

## Configuration GUI

Run the GUI to update the webhook URL, key, schedule and message text:

```bash
python3 config_gui.py
```

Changes are written to `config.json` which the daemon reads automatically.

## Packaging for Windows

On Windows, install `pywin32` and `pyinstaller` and build the service
executable:

```bash
pip install pywin32 pyinstaller
pyinstaller --onefile --noconsole --name WeChatDaemon_Setup win_service.py
```

Run the resulting `WeChatDaemon_Setup.exe` with the `install` argument to
register the service and `start` to run it:

```bash
WeChatDaemon_Setup.exe install
WeChatDaemon_Setup.exe start
```

You can also package `config_gui.py` to provide a graphical configuration
tool:

```bash
pyinstaller --windowed --name WeChatDaemon_Config config_gui.py
```
