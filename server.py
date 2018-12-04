

class Server:

    connected_sockets = []
    encoding = "utf-8"  # кодировка информации
    port = 9090  # Будем принимать подключение в порт с таким номером
    host = ''  # Подключение принимаем от люього компьютера в сети
    mes_size = 1024  # размер сообщения
    max_queue = 2  # - максимальный размер очереди - 2, т.к. будет только два подключения

    def __init__(self):
        import socket
        # создаем сокет, раюотающий по протоколу TCP
        self.server_socket = socket.socket()
        # (хост, порт) = хост - машина которую мы слушаем, если не указана, то принимаются связи от всех машин,
        # порт - номер порта который принимает соединение
        self.server_socket.bind((self.host, self.port))
        #  число соединений, которые будут находиться в очереди соединений до вызова accept
        self.server_socket.listen(self.max_queue)

    def send_data(self, client, address):
        while True:
            data = client.recv(self.mes_size)
            for other_conn in self.connected_sockets:
                if other_conn == client:
                    continue
                other_conn.send(data)
            if not data:
                client.close()
                print("disconnected:", address)
                self.connected_sockets.remove(client)

    def run(self):
        import threading
        while True:

            connected_socket, connected_addres = self.server_socket.accept()
            print("connected:", connected_addres)
            self.connected_sockets.append(connected_socket)
            connected_socket.send(bytes("your ID: " + str(len(self.connected_sockets)) + "\n", self.encoding))

            send_thread = threading.Thread(target=self.send_data, args=(connected_socket, connected_addres))
            send_thread.setDaemon(True)
            send_thread.start()


def main():
    server = Server()
    server.run()


if __name__ == '__main__':
    main()

