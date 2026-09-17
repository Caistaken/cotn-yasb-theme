import socket
import sys

TCP_PORT = 5056

def trigger():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        s.connect(("127.0.0.1", TCP_PORT))
        s.sendall(b"toggle")
        s.close()
    except Exception:
        pass

if __name__ == "__main__":
    trigger()
    sys.exit(0)