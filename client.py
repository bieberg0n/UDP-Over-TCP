import socket
from threading import Thread
import config
from utils import recv, log, info


class Client:
    def __init__(self):
        self.c = socket.socket(2, 2)
        self.c.bind(config.client_listen_addr)
        self.s = socket.socket()
        self.s.connect(config.server_listen_addr)
        self.game_addr = None

    def relay(self, tcp_conn, udp_conn):
        while True:
            data = recv(tcp_conn)
            log('server -> local:', data)
            udp_conn.sendto(data, self.game_addr)

    # def handle(self, conn):
    #     c = socket.socket(2, 2)
    #     t = Thread(target=self.relay, args=(c, conn))
    #     t.setDaemon(True)
    #     t.start()
    #     while True:
    #         data = recv(conn)
    #         c.sendto(data, config.remote_udp)

    def run(self):
        info('UDP Over TCP Client start on', config.client_listen_addr)
        t = Thread(target=self.relay, args=(self.s, self.c))
        t.setDaemon(True)
        t.start()
        # relay_start = False
        while True:
            data, self.game_addr = self.c.recvfrom(4096)
            # if not relay_start:

            log('local -> server:', data)
            self.s.sendall(str(len(data)).encode() + b'\n' + data)


def main():
    c = Client()
    c.run()


if __name__ == '__main__':
    main()
