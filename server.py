# -*- coding: utf-8 -*-

import socket
import threading
import Queue
import time
import json
import sql


class Server:

    # SOCKET ------------------------------------------------------------------
    def config(self):
        self.connection_server = ("", 514)
        self.connections = {} #example: {"port" : [connectio_obj, thread_obj}
        # self.data_clients = {} #temp client data: {"id": data}
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind(self.connection_server)
        self.socket_server.listen(300)
        # self.hold_listen_server = Queue.Queue(1)
        # self.lock = threading

    def admin(self):
        while True:
            cmmd = raw_input(">")
            if cmmd == "list":
                print "[CONN]:", self.connections.keys()
            elif cmmd == "list2":
                print "[CONN]:", self.connections.keys()

    def listen(self):
        c_socket, address = self.socket_server.accept()
        c_port = str(address[1])
        client = Connection(c_socket, c_port)
        return client

    def start_th(self,target, args = (), daemon = False):
        th = threading.Thread(target = target, args = args)
        th.setDaemon(daemon)
        th.start()

    def depure(self):
        time.sleep(1)
        for i in self.connections.keys():
            th = self.connections[i][1]
            if not th.is_alive():
                try:
                    (self.connections[i][0]).socket.close()
                except Exception as err:
                    print err
                    pass
                del self.connections[i]

    # DATA --------------------------------------------------------------------
    def jsontree(self, message, indent = 2):
        if type(message) is unicode:
            message = json.loads(message)
        message = json.dumps(message, sort_keys = True, indent = indent)
        return message

    def insertdb(self, message):
        """{"<QINFO>": [
                ["2017-01-10 12:30:15", 10,20,30],
                ["2017-01-10 12:30:15", 10,20,30]],
            "code": "FS053"}"""

        rawdata = json.loads(message)
        code = rawdata["code"]
        dtype = rawdata.keys()[0]

        if dtype == "<QINFO>":
            data = rawdata["<QINFO>"]
            try:
                sql.insert_qinfo(data, code)
            except Exception as err:
                print "[EXECEPTION]:", err  # [LOG]

        elif dtype == "<INFO>":
            data = rawdata["<INFO>"]
            try:
                # print data # [DEBUG]
                sql.insert_info(data, code)
            except Exception as err:
                print "[EXECEPTION]:", err  # [LOG]



class Connection:

    def __init__(self, c_socket, c_port):
        self.socket = c_socket
        self.port = c_port
        self.hold_c = Queue.Queue(1)

    def hold(self):
        self.hold_c.get(block = True, timeout = None)

    def close(self):
        self.hold_c.put("", block = True, timeout = None)
        self.socket.close()
