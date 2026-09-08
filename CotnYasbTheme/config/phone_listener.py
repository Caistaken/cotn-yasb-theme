import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA_FILE = os.path.expanduser(r"~\.config\yasb\phone_notifications.json")

class NotificationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode("utf-8"))
            app = payload.get("app", "").strip()
            title = payload.get("title", "").strip()
            msg = payload.get("message", "").strip()

            invalid_placeholders = {"[not_body]", "[not_text]", "[notification_text]", "null", "None"}
            if msg in invalid_placeholders:
                msg = ""
            if title in invalid_placeholders:
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
        except Exception:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5055), NotificationHandler)
    server.serve_forever()