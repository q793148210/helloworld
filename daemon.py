import json
import os
import time
from datetime import datetime

from quantum_messaging import QuantumMessagingAPI

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "webhook_url": "",
    "key": "",
    "proxies": None,
    "message": "Hello from Quantum Messaging",
    "schedule": [
        {"days": [0, 2], "time": "09:00"}  # Monday=0, Wednesday=2
    ],
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def message_due(config, now, sent_flags):
    weekday = now.weekday()
    current_time = now.strftime("%H:%M")
    for idx, item in enumerate(config.get("schedule", [])):
        if weekday in item.get("days", []) and current_time == item.get("time"):
            # avoid sending multiple times within the same minute
            if sent_flags.get(idx) != current_time:
                sent_flags[idx] = current_time
                return True
    return False


def run_daemon(stop_event=None):
    """Run the messaging loop until ``stop_event`` is set."""
    sent_flags = {}
    while not (stop_event and getattr(stop_event, "is_set", lambda: False)()):
        config = load_config()
        api = QuantumMessagingAPI(
            config.get("webhook_url"),
            config.get("key"),
            proxies=config.get("proxies"),
        )
        now = datetime.now()
        if message_due(config, now, sent_flags):
            api.send_text_message(config.get("message", ""))
        for _ in range(30):
            if stop_event and getattr(stop_event, "is_set", lambda: False)():
                break
            time.sleep(1)


def main():
    """Entry point for running the daemon as a regular script."""
    class Dummy:
        def is_set(self):
            return False

    run_daemon(Dummy())


if __name__ == "__main__":
    main()
