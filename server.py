import socket
from threading import Thread
import config
from utils import recv, log, info


class Server:
    def __init__(self):
        self.s = socket.socket()
        self.s.bind(config.server_listen_addr)
        self.s.listen(5)

    def relay(self, c, conn):
        while True:
            data, _ = c.recvfrom(4096)
            log('remote -> client:', data)
            conn.sendall(str(len(data)).encode() + b'\n' + data)

    def handle(self, conn):
        c = socket.socket(2, 2)
        c.connect(config.remote_udp)
        # relay_started = False
        t = Thread(target=self.relay, args=(c, conn))
        t.setDaemon(True)
        t.start()
        while True:
            data = recv(conn)
            log('client -> remote:', data)
            c.sendto(data, config.remote_udp)
            # if not relay_started:
            #     relay_started = True

    def run(self):
        info('UDP Over TCP Server start on', config.server_listen_addr)
        info('Server will relay data to', config.remote_udp)
        while True:
            conn, addr = self.s.accept()
            t = Thread(target=self.handle, args=(conn,))
            t.setDaemon(True)
            log(addr, 'connect in')
            t.start()


def main():
    s = Server()
    s.run()


if __name__ == '__main__':
    main()
