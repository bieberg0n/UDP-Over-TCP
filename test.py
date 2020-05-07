import time
import socket


def main():
    test = b'test'
    test2 = b'abcde'

    udp_s = socket.socket(2, 2)
    udp_s.bind(('127.0.0.1', 2020))
    udp_c = socket.socket(2, 2)

    while True:
        udp_c.sendto(test, ('127.0.0.1', 2021))
        time.sleep(0.2)
    # udp_c.sendto(test, ('127.0.0.1', 2021))

    # data, addr = udp_s.recvfrom(2048)
    # assert data == test

    # udp_s.sendto(test2, addr)
    # data, addr = udp_c.recvfrom(512)
    # assert data == test2


if __name__ == '__main__':
    main()
