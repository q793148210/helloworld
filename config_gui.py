import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

from quantum_messaging import QuantumMessagingAPI

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "webhook_url": "",
    "key": "",
    "proxies": None,
    "message": "Hello from Quantum Messaging",
    "schedule": [{"days": [0, 2], "time": "09:00"}],
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


class ConfigApp(tk.Tk):
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self):
        super().__init__()
        self.title("企业微信推送配置")
        self.resizable(False, False)
        self.cfg = load_config()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text="Webhook URL:").grid(row=0, column=0, sticky="e")
        self.webhook_var = tk.StringVar(value=self.cfg.get("webhook_url", ""))
        ttk.Entry(frame, textvariable=self.webhook_var, width=40).grid(row=0, column=1)

        ttk.Label(frame, text="Key:").grid(row=1, column=0, sticky="e")
        self.key_var = tk.StringVar(value=self.cfg.get("key", ""))
        ttk.Entry(frame, textvariable=self.key_var, width=40).grid(row=1, column=1)

        ttk.Label(frame, text="Message:").grid(row=2, column=0, sticky="e")
        self.msg_var = tk.StringVar(value=self.cfg.get("message", ""))
        ttk.Entry(frame, textvariable=self.msg_var, width=40).grid(row=2, column=1)

        ttk.Label(frame, text="Send Days:").grid(row=3, column=0, sticky="ne")
        day_frame = ttk.Frame(frame)
        day_frame.grid(row=3, column=1, sticky="w")
        self.day_vars = []
        days_selected = set(self.cfg.get("schedule", [{}])[0].get("days", []))
        for idx, name in enumerate(self.DAYS):
            var = tk.BooleanVar(value=idx in days_selected)
            self.day_vars.append(var)
            ttk.Checkbutton(day_frame, text=name, variable=var).grid(row=0, column=idx, sticky="w")

        ttk.Label(frame, text="Time (HH:MM):").grid(row=4, column=0, sticky="e")
        self.time_var = tk.StringVar(value=self.cfg.get("schedule", [{}])[0].get("time", "09:00"))
        ttk.Entry(frame, textvariable=self.time_var, width=10).grid(row=4, column=1, sticky="w")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=1, pady=5, sticky="e")
        ttk.Button(btn_frame, text="Save", command=self.save).grid(row=0, column=0, padx=(0,5))
        ttk.Button(btn_frame, text="Test", command=self.send_test).grid(row=0, column=1)

    def save(self):
        self.cfg["webhook_url"] = self.webhook_var.get()
        self.cfg["key"] = self.key_var.get()
        self.cfg["message"] = self.msg_var.get()
        days = [i for i, v in enumerate(self.day_vars) if v.get()]
        self.cfg["schedule"] = [{"days": days, "time": self.time_var.get()}]
        save_config(self.cfg)
        messagebox.showinfo(title="Saved", message="配置已保存")

    def send_test(self):
        """Send a one-time test message using current form values."""
        api = QuantumMessagingAPI(
            self.webhook_var.get(), self.key_var.get(), proxies=None
        )
        result = api.send_text_message(self.msg_var.get())
        if isinstance(result, dict) and result.get("error"):
            messagebox.showerror(title="Error", message="测试失败: " + result["error"])
        else:
            messagebox.showinfo(title="Success", message="测试消息已发送")


if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()
