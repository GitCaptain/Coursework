
class Client:
    encoding = "utf-8"
    port_to_connect = 9090
    mes_size = 1024

    def __init__(self, use_transport_layer_security=False, use_program_security=False, server_hostname='localhost'):
        import socket

        self.cipher = use_program_security

        self.socket = socket.socket()

        if use_transport_layer_security:
            import ssl
            context = ssl.create_default_context()
            # context.load_verify_locations("server_cert.pem")
            context.load_verify_locations("ssl_cert.pem")
            context.check_hostname = False
            self.socket = context.wrap_socket(self.socket, server_hostname=server_hostname)

        self.socket.connect((server_hostname, self.port_to_connect))

        server_data = self.socket.recv(self.mes_size)
        print("ID:", server_data.strip().split()[2].decode())

    def run(self):
        import threading
        user_thread = threading.Thread(target=self.user_data)
        user_thread.setDaemon(True)
        user_thread.start()

        while True:
            server_data = self.socket.recv(self.mes_size)
            if not server_data:
                break
            print(server_data.decode())

    def user_data(self):
        while True:
            user_data = input()
            if user_data:  # не отсылаем пустую строку, это ломает что-то внутри _ssl.c
                self.socket.send(bytes(user_data, self.encoding))


def main():
    from sys import argv

    address = '192.168.1.33'
    tls = False
    cipher = False

    for arg in argv[1:]:
        if arg == '--tls':
            tls = True
        elif arg == '--cipher':
            cipher = True
        else:
            address = arg

    client = Client(tls, cipher, address)
    client.run()


if __name__ == '__main__':
    main()
