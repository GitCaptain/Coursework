
class Client:
    encoding = "utf-8"
    port_to_connect = 9090
    mes_size = 1024

    def __init__(self):
        import socket
        import ssl

        self.sock = socket.socket()
        self.sock.connect(('localhost', self.port_to_connect))
        server_data = self.sock.recv(self.mes_size)
        print("ID:", server_data.strip().split()[2].decode())

    def run(self):
        import threading
        user_thread = threading.Thread(target=self.user_data)
        user_thread.setDaemon(True)
        user_thread.start()

        while True:
            server_data = self.sock.recv(self.mes_size)
            if not server_data:
                break
            print(server_data.decode())

    def user_data(self):
        while True:
            user_data = input()
            self.sock.send(bytes(user_data, self.encoding))


def main():
    client = Client()
    client.run()


if __name__ == '__main__':
    main()
