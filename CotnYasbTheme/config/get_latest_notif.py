import sys
import json
import os
import subprocess

sys.stdout.reconfigure(encoding="utf-8")

CONFIG_DIR = os.path.expanduser(r"~\.config\yasb")
DATA_FILE = os.path.join(CONFIG_DIR, "phone_notifications.json")
LOCK_FILE = os.path.join(CONFIG_DIR, ".service_spawned")

APP_ICONS = {
    "whatsapp": "\uf232",
    "x": "\ue61b",
    "twitter": "\ue61b",
    "instagram": "\uf16d",
    "discord": "\udb81\udf5a",
    "telegram": "\uf2c6",
    "messages": "\udb80\udf67",
    "mail": "\uf0e0",
    "default": "\uf0f3"
}

def ensure_services():
    if not os.path.exists(LOCK_FILE):
        subprocess.Popen(["pyw", os.path.join(CONFIG_DIR, "phone_listener.py")], creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["pyw", os.path.join(CONFIG_DIR, "show_popup.py")], creationflags=subprocess.CREATE_NO_WINDOW)
        with open(LOCK_FILE, "w") as f:
            f.write("1")

def get_icon(app_name):
    clean = app_name.lower().strip()
    for key, icon in APP_ICONS.items():
        if key in clean:
            return icon
    return APP_ICONS["default"]

def format_notification():
    ensure_services()
    if not os.path.exists(DATA_FILE):
        return "\uf0f3 Bildirim yok"

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                return "\uf0f3 Bildirim yok"

            latest = data[0]
            app = latest.get("app", "")
            title = latest.get("title", "")
            msg = latest.get("message", "")

            icon = get_icon(app)
            content = f"{title}: {msg}" if msg else title
            if len(content) > 28:
                content = content[:25] + "..."

            return f"{icon}  {app}: {content}"
    except Exception:
        return "\uf0f3 Bildirim yok"

if __name__ == "__main__":
    print(format_notification())
