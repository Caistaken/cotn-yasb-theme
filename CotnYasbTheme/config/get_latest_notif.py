import sys
import json
import os

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CONFIG_DIR = os.path.expanduser(r"~\.config\yasb")
DATA_FILE = os.path.join(CONFIG_DIR, "phone_notifications.json")
PRIVACY_FILE = os.path.join(CONFIG_DIR, ".bar_privacy_mode")

APP_ICONS = {
    "whatsapp": "\uf232",
    "x": "\ue61b",
    "twitter": "\ue61b",
    "instagram": "\uf16d",
    "discord": "\uf392",
    "telegram": "\uf2c6",
    "messages": "\uf0e0",
    "mail": "\uf0e0",
    "twitch": "\uf1e8",
    "youtube": "\uf167",
    "default": "\uf0f3"
}

def get_icon(app_name):
    clean = str(app_name).lower().strip()
    for key, icon in APP_ICONS.items():
        if key in clean:
            return icon
    return APP_ICONS["default"]

def toggle_privacy():
    try:
        if os.path.exists(PRIVACY_FILE):
            os.remove(PRIVACY_FILE)
        else:
            with open(PRIVACY_FILE, "w", encoding="utf-8") as f:
                f.write("1")
    except Exception:
        pass

def format_notification():
    if not os.path.exists(DATA_FILE):
        return "\uf0f3 No notifications"

    try:
        with open(DATA_FILE, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
            if not data:
                return "\uf0f3 No notifications"

            latest = data[0]
            app = str(latest.get("app", "")).strip()
            title = str(latest.get("title", "")).strip()
            msg = str(latest.get("message", "")).strip()
            icon = get_icon(app)

            if os.path.exists(PRIVACY_FILE):
                return f"\uf023  {icon} {app}: ••••••"

            content = f"{title}: {msg}" if msg else title
            if len(content) > 28:
                content = content[:25] + "..."
            return f"{icon}  {app}: {content}"
    except Exception:
        return "\uf0f3 No notifications"

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--toggle-privacy":
        toggle_privacy()
        sys.exit(0)
    try:
        print(format_notification())
    except Exception:
        print("\uf0f3 No notifications")