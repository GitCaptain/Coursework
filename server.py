

class Server:

    connected_sockets = []
    encoding = "utf-8"  # кодировка информации
    port = 9090  # Будем принимать подключение в порт с таким номером
    host = ''  # Подключение принимаем от любого компьютера в сети
    mes_size = 1024  # размер сообщения
    max_queue = 2  # - максимальный размер очереди - 2, т.к. будет только два подключения

    def __init__(self, use_transport_layer_security=False):
        import socket
        # создаем сокет, работающий по протоколу TCP
        self.server_socket = socket.socket()
        # (хост, порт) = хост - машина которую мы слушаем, если не указана, то принимаются связи от всех машин,
        # порт - номер порта который принимает соединение
        self.server_socket.bind((self.host, self.port))
        self.tls = use_transport_layer_security
        #  число соединений, которые будут находиться в очереди соединений до вызова accept
        self.server_socket.listen(self.max_queue)

        if use_transport_layer_security:
            import ssl
            self.context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            # self.context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
            self.context.load_cert_chain(certfile="ssl_cert.pem")

    def send_data(self, client, address):
        try:
            while True:
                data = client.recv(self.mes_size)
                for other_conn in self.connected_sockets:
                    if other_conn == client:
                        continue
                    other_conn.send(data)
        except:
            pass
        finally:
            client.close()
            print("disconnected:", address)
            self.connected_sockets.remove(client)

    def run(self):
        print("the server is running")
        import threading
        while True:

            connected_socket, connected_addres = self.server_socket.accept()
            if self.tls:
                connected_socket = self.context.wrap_socket(connected_socket, server_side=True)
            print("connected:", connected_addres)
            self.connected_sockets.append(connected_socket)
            connected_socket.sendall(bytes("your ID: " + str(len(self.connected_sockets)) + "\n", self.encoding))

            send_thread = threading.Thread(target=self.send_data, args=(connected_socket, connected_addres))
            send_thread.setDaemon(True)
            send_thread.start()


def main():
    from sys import argv
    tls = False
    if '--tls' in argv:
        tls = True
    server = Server(tls)
    server.run()


if __name__ == '__main__':
    main()

