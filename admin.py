# -*- coding: utf-8 -*-

import socket
import Queue
import time
import json
import psutil


class Admin:
    def vars(self):
        self.connection_server = ("kraken.fintra.co", 514)
        self.hold_connection = Queue.Queue(1)

    def connection(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(self.connection_server)

    def listen(self):
        message = self.socket_client.recv(1024)
        return message

    def send(self,message):
        self.socket_client.send(message)

    def listen(self):
        while True:
            message = self.socket_client.recv(1024)
            return message

    def process(self, message):
        #cerrar conexion
        if message == "":
            self.close()
        elif message == "close":
            self.close()
        else:
            print message



    def qinfo(self):

        def sayhi():
            temp = socket.gethostbyname_ex(socket.gethostname())
            name = temp[0]
            ip = tuple(temp[2])
            return name, ip

        def hddusage():
            temp = psutil.disk_partitions()[0]
            if temp[0][0] == "C":
                temp = psutil.disk_usage(temp[0])[3]
            else:
                temp = 0
            return temp

        name, ip = sayhi()
        cpu = psutil.cpu_percent(interval=60)
        ram = psutil.virtual_memory()[2]
        hdd = hddusage()

        header = self.header("<QINFO>")
        message = [name, ip, cpu, ram, hdd]

        return [header, message]


    def header(self,type,respond = False):
        type = type
        timedate = time.strftime("%d%m%y%H%M%S")
        return [type, timedate, respond]


    def formatout(self,message):
        message = json.dumps(message,)
        return message

    def disconnect(self):
        self.socket_client.close()
