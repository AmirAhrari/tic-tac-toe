import socket


class Client:
    def __init__(self, host="127.0.0.1", port=9009):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")
        self.sock.connect((self.host, self.port))
        print(f"Connected to {self.host}:{self.port}")

    def send(self, message):
        self.sock.send(message.encode("utf-8"))

    def recv(self):
        data = self.sock.recv(1024)
        return data.decode("utf-8")
