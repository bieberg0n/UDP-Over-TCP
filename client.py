import socket
from threading import Thread
import config
from utils import recv, log, info, spawn


class Client:
    def __init__(self):
        self.c = socket.socket(2, 2)
        self.c.bind(config.client_listen_addr)

        self.game_addr = None

    def relay(self, tcp_conn, udp_conn):
        while True:
            data = recv(tcp_conn)
            log('server -> local:', data)
            if data is None:
                tcp_conn.close()
                return
            udp_conn.sendto(data, self.game_addr)

    def run(self):
        s = socket.socket()
        s.connect(config.server_listen_addr)
        # t = Thread(target=self.relay, args=(s, self.c))
        # t.setDaemon(True)
        # t.start()
        spawn(target=self.relay, args=(s, self.c))

        while True:
            data, self.game_addr = self.c.recvfrom(4096)
            log('local -> server:', data)
            s.sendall(str(len(data)).encode() + b'\n' + data)

    def supervisor(self):
        info('UDP Over TCP Client start on', config.client_listen_addr)
        while True:
            t = spawn(target=self.run)
            t.join()
            info('Reconnect...')


def main():
    c = Client()
    c.supervisor()


if __name__ == '__main__':
    main()
