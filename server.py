
class Server:

    connected_sockets = []  # список подключенных сокетов
    encoding = "utf-8"  # кодировка информации
    port = 9093  # Будем принимать подключение в порт с таким номером
    host = ''  # Подключение принимаем от любого компьютера в сети
    mes_size = 2048  # максимальный размер сообщения
    max_queue = 5  # число соединений, которые будут находиться в очереди соединений до вызова accept
    # список команд доступных для сервера
    commands = ['/commands - показать список команд и их описание',
                '/end - остановить работу сервера']

    def __init__(self, use_transport_layer_security=False):
        import socket

        # создаем сокет, работающий по протоколу TCP

        self.server_socket = socket.socket()
        # (хост, порт) = хост - машина которую мы слушаем, если не указана, то принимаются связи от всех машин,
        # порт - номер порта который принимает соединение
        self.server_socket.bind((self.host, self.port))
        self.tls = use_transport_layer_security
        self.server_socket.listen(self.max_queue)
        self.users_online = 0
        if use_transport_layer_security:
            # если используем ssl нужно создать контекст для обертки сокетов
            import ssl
            self.context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            # self.context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
            self.context.load_cert_chain(certfile="ssl_cert.pem")

    def send_data(self, client, address, client_id):
        try:
            while True:
                data = client.recv(self.mes_size)
                if not data:
                    break
                for other_conn in self.connected_sockets:
                    if other_conn == client:
                        continue
                    other_conn.send(data)
        except Exception as e:
            pass
            #print(e)
        finally:
            client.shutdown(2)
            client.close()
            self.connected_sockets.remove(client)
            print("disconnected:", address)
            self.users_online -= 1
            print("users online:", self.users_online)

    # нужно научиться нормально завершать сервер
    def server_command_handler(self):
        while True:
            command = input()
            if not command.startswith('/'):
                continue
            if command == '/commands':
                for c in self.commands:
                    print(c)
            if command == '/end':
                print("server stopped")
                self.server_socket.shutdown(2)
                self.server_socket.close()
                for c in self.connected_sockets:
                    c.shutdown(2)
                    c.close()
                self.connected_sockets.clear()
                break

    def run(self):
        import threading

        command_handler = threading.Thread(target=self.server_command_handler)
        command_handler.setDaemon(True)
        command_handler.start()

        print("type /commands to see a list of available commands")

        print("the server is running")

        while True:

            connected_socket, connected_addres = self.server_socket.accept()
            if self.tls:
                connected_socket = self.context.wrap_socket(connected_socket, server_side=True)
            print("connected:", connected_addres)
            self.users_online += 1
            print("users online:", self.users_online)
            self.connected_sockets.append(connected_socket)
            ID = str(len(self.connected_sockets))
            connected_socket.sendall(bytes("your ID: " + ID + "\n", self.encoding))

            send_thread = threading.Thread(target=self.send_data, args=(connected_socket, connected_addres, ID))
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

