# -*- coding: utf-8 -*-

import server
import threading
import logging


class MethodServer(server.Server):

    def __init__(self):
        self.config()
        logging.basicConfig(filename = 'server.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s - %(name)-13s: %(levelname)-8s - %(message)s')
        logging.info(self.name)

    def run(self):
        logger = logging.getLogger("run")
        self.start_th(self.listen_method)
        logger.debug("th listen_method iniciado")
        self.start_th(self.depure_method)
        logger.debug("th depure_method iniciado")
        self.start_th(self.admin)
        logger.debug("th admin iniciado")

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
        logger = logging.getLogger("connection_daemon")
        try:
            client = self.connections[c_port][0]
            message = client.socket.recv(102400)
            logger.debug("mensaje recivido de " + c_port)
            self.process_method(message, c_port)
            client.close()
        except Exception as err:
            logger.warning(err)
            pass

    def process_method(self, message, c_port):
        logger = logging.getLogger("process_method")
        client = self.connections[c_port][0]

        if "INFO>" in message:
            self.insertdb(message)
        else:
            client.close()

        return 0


    def depure_method(self):
        while True:
            self.depure()
