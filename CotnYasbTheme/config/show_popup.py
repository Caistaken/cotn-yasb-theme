import sys
import json
import os
import socket
import threading
import ctypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QFrame, QScrollArea, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QCursor

DATA_FILE = os.path.expanduser(r"~\.config\yasb\phone_notifications.json")
TCP_PORT = 5056
HTTP_PORT = 5055

VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
user32 = ctypes.windll.user32

class TriggerSignal(QObject):
    toggle = pyqtSignal()
    data_updated = pyqtSignal()

trigger = TriggerSignal()

class NotificationHttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        try:
            payload = json.loads(post_data.decode("utf-8"))
            app = payload.get("app", "").strip()
            title = payload.get("title", "").strip()
            msg = payload.get("message", "").strip()

            invalid = {"[not_body]", "[not_text]", "[notification_text]", "null", "None"}
            if msg in invalid:
                msg = ""
            if title in invalid:
                title = ""

            cleaned = {
                "app": app if app else "Notification",
                "title": title,
                "message": msg
            }

            history = []
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []

            history.insert(0, cleaned)
            history = history[:15]

            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            trigger.data_updated.emit()
        except Exception:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass

class FastNotificationPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Tool | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(340)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.container = QFrame()
        self.container.setObjectName("mainContainer")
        self.container.setStyleSheet("""
            QFrame#mainContainer {
                background-color: rgba(12, 12, 16, 0.98);
                border: 1px solid rgba(255, 255, 255, 0.16);
                border-radius: 8px;
            }
        """)
        self.c_layout = QVBoxLayout(self.container)
        self.c_layout.setContentsMargins(14, 12, 14, 12)
        self.c_layout.setSpacing(8)

        header_bar = QHBoxLayout()
        header_bar.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("Notification History")
        title_label.setStyleSheet("""
            color: #f3f4f6;
            font-size: 12px;
            font-weight: 700;
            border: none;
            font-family: 'SpaceMono Nerd Font', monospace;
        """)

        self.clear_all_btn = QPushButton("Clear")
        self.clear_all_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #71717a;
                border: none;
                font-size: 11px;
                font-weight: 600;
                font-family: 'SpaceMono Nerd Font', monospace;
                padding: 2px 6px;
                border-radius: 4px;
            }
            QPushButton:hover {
                color: #ef4444;
                background-color: rgba(239, 68, 68, 0.1);
            }
        """)
        self.clear_all_btn.clicked.connect(self.clear_all_notifications)

        header_bar.addWidget(title_label)
        header_bar.addStretch()
        header_bar.addWidget(self.clear_all_btn)
        self.c_layout.addLayout(header_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.03);
                width: 4px;
                margin: 0px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(196, 181, 253, 0.35);
                min-height: 20px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(196, 181, 253, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.scroll_widget)
        self.list_layout.setContentsMargins(0, 0, 4, 0)
        self.list_layout.setSpacing(6)

        self.scroll.setWidget(self.scroll_widget)
        self.c_layout.addWidget(self.scroll)
        main_layout.addWidget(self.container)

        self.watch_timer = QTimer(self)
        self.watch_timer.setInterval(40)
        self.watch_timer.timeout.connect(self.check_outside_click)

    def check_outside_click(self):
        if not self.isVisible():
            self.watch_timer.stop()
            return
        left_down = user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000
        right_down = user32.GetAsyncKeyState(VK_RBUTTON) & 0x8000
        if left_down or right_down:
            if not self.geometry().contains(QCursor.pos()):
                self.hide()
                self.watch_timer.stop()

    def showEvent(self, event):
        super().showEvent(event)
        self.watch_timer.start()

    def hideEvent(self, event):
        self.watch_timer.stop()
        super().hideEvent(event)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_data(self, data):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def delete_notification(self, index):
        notifications = self.load_data()
        if 0 <= index < len(notifications):
            notifications.pop(index)
            self.save_data(notifications)
            self.refresh_content()

    def clear_all_notifications(self):
        self.save_data([])
        self.refresh_content()

    def refresh_content(self):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        notifications = self.load_data()

        if notifications:
            self.clear_all_btn.show()
            for idx, n in enumerate(notifications):
                card = QFrame()
                card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(255, 255, 255, 0.04);
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        border-radius: 6px;
                    }
                """)
                card_layout = QVBoxLayout(card)
                card_layout.setContentsMargins(10, 8, 10, 8)
                card_layout.setSpacing(4)

                top_row = QHBoxLayout()
                top_row.setContentsMargins(0, 0, 0, 0)

                app_name = n.get("app", "Notification")
                title_text = n.get("title", "")
                header_text = f"{app_name} • {title_text}".strip(" •")
                
                app_title = QLabel(header_text)
                app_title.setStyleSheet("""
                    color: #c4b5fd;
                    font-weight: 700;
                    font-size: 11px;
                    border: none;
                    font-family: 'SpaceMono Nerd Font', monospace;
                """)

                del_btn = QPushButton("✕")
                del_btn.setFixedSize(16, 16)
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: #71717a;
                        border: none;
                        font-size: 10px;
                        font-weight: bold;
                        padding: 0px;
                        margin: 0px;
                    }
                    QPushButton:hover {
                        color: #ef4444;
                    }
                """)
                del_btn.clicked.connect(lambda _, i=idx: self.delete_notification(i))

                top_row.addWidget(app_title)
                top_row.addStretch()
                top_row.addWidget(del_btn)
                card_layout.addLayout(top_row)

                msg_str = n.get("message", "").strip()
                if msg_str:
                    msg = QLabel(msg_str)
                    msg.setWordWrap(True)
                    msg.setStyleSheet("""
                        color: #d1d5db;
                        font-size: 11px;
                        border: none;
                        font-family: 'SpaceMono Nerd Font', monospace;
                    """)
                    card_layout.addWidget(msg)

                self.list_layout.addWidget(card)

            self.list_layout.addStretch()
            self.setMaximumHeight(360)
            self.adjustSize()
        else:
            self.clear_all_btn.hide()
            empty = QLabel("No notifications yet.")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("""
                color: #71717a;
                font-size: 11px;
                border: none;
                font-family: 'SpaceMono Nerd Font', monospace;
            """)
            self.list_layout.addWidget(empty)
            self.setFixedHeight(100)

    def toggle_popup(self):
        if self.isVisible():
            self.hide()
        else:
            self.refresh_content()
            self.move(122, 46)
            self.show()
            self.raise_()
            self.activateWindow()

def run_http_server():
    server = HTTPServer(("0.0.0.0", HTTP_PORT), NotificationHttpHandler)
    server.serve_forever()

def run_tcp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", TCP_PORT))
    s.listen(5)
    while True:
        try:
            conn, _ = s.accept()
            data = conn.recv(16)
            if b"toggle" in data:
                trigger.toggle.emit()
            conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)

    popup = FastNotificationPopup()
    trigger.toggle.connect(popup.toggle_popup)
    trigger.data_updated.connect(popup.refresh_content)

    t_http = threading.Thread(target=run_http_server, daemon=True)
    t_http.start()

    t_tcp = threading.Thread(target=run_tcp_server, daemon=True)
    t_tcp.start()

    sys.exit(app.exec())