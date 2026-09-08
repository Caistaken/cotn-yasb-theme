# Cotn Yasb Theme + Phone Notification Bridge 🌙📱

A clean, dark, monochrome YASB (Yet Another Status Bar) setup featuring an ultra-low latency Android notification mirror and an interactive popup history panel.

## Features

- **Local Network Notification Bridge:** Receive instant alerts from apps like WhatsApp, X (Twitter), Instagram, and Discord directly on your status bar.
- **Zero-Latency History Panel:** Fast PyQt6 popup that toggles instantly and dismisses on focus loss.
- **Dynamic Window Sizing:** Compact 100px footprint when empty, dynamically expanding up to 360px as notifications arrive.
- **Granular Controls:** Clear all notifications or dismiss individual entries.
- **Headless Background Services:** Runs cleanly via background daemons without persistent command prompt windows.

---

## Prerequisites & Recommendations

- [YASB (Yet Another Status Bar)](https://github.com/amnweb/yasb)
- Python 3.10+ installed and added to `PATH`
- [SpaceMono Nerd Font](https://www.nerdfonts.com/) (Strongly recommended for status bar icons and monospaced alignment)

---

## Installation

> **Note:** Running `install.bat` will copy files into `%USERPROFILE%\.config\yasb`. Back up your existing YASB configuration if you have one.

1. Clone or download the repository:
   ```bash
   git clone [https://github.com/your-username/CotnYasbTheme.git](https://github.com/your-username/CotnYasbTheme.git)
   cd CotnYasbTheme