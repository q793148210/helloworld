# Hello World

This repository includes a simple C program and a Python daemon for sending
scheduled messages via Quantum Messaging.

## Files

- `hello.c` – example C source.
- `quantum_messaging.py` – library for sending messages.
- `daemon.py` – reads `config.json` and sends messages at the configured times.
- `config.json` – configuration file created on first run if missing.

## Running the daemon

Edit `config.json` to provide your webhook URL and key. The default schedule
sends a message every Monday and Wednesday at 09:00. Start the daemon with:

```bash
python3 daemon.py
```

The daemon reloads configuration on each cycle so edits to `config.json`
take effect automatically.
