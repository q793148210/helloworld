import json
import os
import time
from datetime import datetime

from quantum_messaging import QuantumMessagingAPI

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "webhook_url": "",
    "key": "",
    "proxies": None,
    "message": "Hello from Quantum Messaging",
    "schedule": [
        {"days": [0, 2], "time": "09:00"}  # Monday=0, Wednesday=2
    ],
    "mention_type": 0,
    "mention_list": [],
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
        if "proxies" not in cfg:
            cfg["proxies"] = DEFAULT_CONFIG["proxies"]
        if "mention_type" not in cfg:
            cfg["mention_type"] = DEFAULT_CONFIG["mention_type"]
        if "mention_list" not in cfg:
            cfg["mention_list"] = DEFAULT_CONFIG["mention_list"]
        return cfg


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
            msg = config.get("message", "")
            m_type = config.get("mention_type", 0)
            if m_type == 0:
                api.send_text_message(msg)
            elif m_type == 1:
                api.send_text_message_with_mention(msg, 1)
            else:
                api.send_text_message_with_mention(msg, m_type, config.get("mention_list", []))
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
