import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 5056))
    s.sendall(b"toggle")
    s.close()
except Exception:
    pass