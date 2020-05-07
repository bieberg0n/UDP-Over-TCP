import socket
from threading import Thread
import config
from utils import recv, log, info, rand_err, spawn


class Server:
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(config.server_listen_addr)
        self.s.listen(5)
        self.udp_client_pool = {}

    def relay(self, c, conn):
        while True:
            data, _ = c.recvfrom(4096)
            log('remote -> client:', data)
            conn.sendall(str(len(data)).encode() + b'\n' + data)

    def udp_client(self, addr):
        ip = addr[0]
        c = self.udp_client_pool.get(ip)
        if not c:
            c = socket.socket(2, 2)
            c.connect(config.remote_udp)
            self.udp_client_pool[ip] = c
            log('udp client pool add')
        return c

    def handle(self, conn, addr):
        c = self.udp_client(addr)
        # t = Thread(target=self.relay, args=(c, conn))
        # t.setDaemon(True)
        # t.start()
        spawn(target=self.relay, args=(c, conn))
        while True:
            data = recv(conn)
            log('client -> remote:', data)
            if (data is None) or rand_err():
                conn.close()
                return
            c.sendto(data, config.remote_udp)

    def run(self):
        info('UDP Over TCP Server start on', config.server_listen_addr)
        info('Server will relay data to', config.remote_udp)
        while True:
            conn, addr = self.s.accept()
            log(addr, 'connect in')
            # t = Thread(target=self.handle, args=(conn, addr))
            # t.setDaemon(True)
            # t.start()
            spawn(target=self.handle, args=(conn, addr))


def main():
    s = Server()
    s.run()


if __name__ == '__main__':
    main()
