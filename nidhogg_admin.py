# -*- coding: utf-8 -*-

import client
import threading


def main():
    cliente = client.Client()
    cliente.connection()

    th = threading.Thread(target = send, args = (cliente,))
    th.start()

    cliente.listen()


def send(cliente):

    def send_child():
        while True:
            cliente.send()

    th = threading.Thread(target = send_child)
    th.setDaemon(True)
    th.start()

    cliente.hold_connection.get(block = True, timeout = None)


if __name__ == '__main__':
    main()