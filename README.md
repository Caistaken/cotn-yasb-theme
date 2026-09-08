# Cotn Yasb Theme + Phone Notification Bridge 🌙📱

A clean, dark, monochrome YASB (Yet Another Status Bar) setup featuring an ultra-low latency Android notification mirror and an interactive popup history panel.

## Features

- Local Network Notification Bridge: Receive instant alerts from apps like WhatsApp, X (Twitter), Instagram, and Discord directly on your status bar.
- Zero-Latency History Panel: Fast PyQt6 popup that toggles instantly and dismisses on focus loss.
- Dynamic Window Sizing: Compact 100px footprint when empty, dynamically expanding up to 360px as notifications arrive.
- Granular Controls: Clear all notifications or dismiss individual entries.
- Headless Background Services: Runs cleanly via background daemons without persistent command prompt windows.

---

## Prerequisites & Recommendations

- YASB (Yet Another Status Bar)
- Python 3.10+ installed and added to PATH
- SpaceMono Nerd Font (Strongly recommended for status bar icons and monospaced alignment)

---

## Installation

> Note: Running install.bat will copy files into %USERPROFILE%\.config\yasb. Back up your existing YASB configuration if you have one.

1. Clone or download the repository:
   git clone [https://github.com/your-username/CotnYasbTheme.git](https://github.com/your-username/CotnYasbTheme.git)
   cd CotnYasbTheme

2. Run install.bat:
   - Automatically installs the required PyQt6 dependency.
   - Copies configuration files directly to %USERPROFILE%\.config\yasb.

3. Launch YASB:
   yasb

---

## Phone Configuration (MacroDroid)

To route notifications from Android to your desktop:

1. Install MacroDroid from Google Play.
2. Ensure both your PC and phone are connected to the same Wi-Fi network.
3. Create a new Macro:
   - Trigger: Notification Received -> Select target applications (e.g., WhatsApp, X, Instagram).
   - Action: HTTP Request
     - Method: POST
     - URL: http://<YOUR_PC_LOCAL_IP>:5055 (Find your PC's IP via ipconfig in CMD/PowerShell)
     - Content Type: application/json
     - Content Body:
       {
         "app": "[not_app_name]",
         "title": "[not_title]",
         "message": "[not_text]"
       }

(Tip: In MacroDroid, use the [...] button to pick [not_app_name], [not_title], and [not_text] directly).

---

## Troubleshooting & Important Notes

- Firewall Notice: If notifications do not register, ensure Windows Defender Firewall allows incoming connections on port 5055, or add Python to your allowed apps.
- Empty Body Alerts: Social apps like X (Twitter) often place all text inside the notification title and leave the message body blank. The built-in listener automatically handles and sanitizes these events.
- Daemon Lifecycle: Background services (phone_listener.py and show_popup.py) are automatically invoked headlessly by YASB on startup.
