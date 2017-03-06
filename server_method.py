# -*- coding: utf-8 -*-

import server
import threading


class MethodServer(server.Server):

    def __init__(self):
        self.config()

    def run(self):
        self.start_th(self.listen_method)
        self.start_th(self.depure_method)
        self.start_th(self.admin())

    def listen_method(self):
        while True:
            client = self.listen()
            self.start_th(self.connection_method, (client,))

    def connection_method(self, client):
        th = threading.current_thread()
        self.connections[client.port] = [client, th]
        self.start_th(self.connection_daemon, (client.port,), True)
        client.hold()


    def connection_daemon(self, c_port):
        client = self.connections[c_port][0]
        message = client.socket.recv(102400)
        self.process_method(message, c_port)
        client.close()

    def process_method(self, message, c_port):
        client = self.connections[c_port][0]

        if message == "":
            client.close()
        elif "<QINFO>" in message:
            self.insertdb(message)
            # self.insertdb.data()
        elif "<INFO>" in message:
            self.insertdb(message)

        return 0


    def depure_method(self):
        while True:
            self.depure()
