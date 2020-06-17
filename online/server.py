import socket


class Server:
    def __init__(self, host="0.0.0.0", port=9009):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def listen(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print(f"Listening on {self.host}:{self.port}")
        self.c1, addr = self.sock.accept()
        print(f"First client has been connected on {addr[0]}:{addr[1]}")
        print("Wating for second client")
        self.c2, addr = self.sock.accept()
        print(f"Second client has been connected on {addr[0]}:{addr[1]}")
        self.send(self.c1, "start")
        self.send(self.c2, "wait")
        print("Starting the game")

    def send(self, sock, message):
        sock.send(message.encode("utf-8"))

    def recv(self, sock):
        data = sock.recv(1024)
        if not data:
            exit()
        return data.decode("utf-8")

    def start(self):
        while True:
            d = self.recv(self.c1)
            self.send(self.c2, d)

            d = self.recv(self.c2)
            self.send(self.c1, d)


if __name__ == "__main__":
    s = Server()
    s.listen()
    s.start()
