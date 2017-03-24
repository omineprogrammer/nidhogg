# -*- coding: utf-8 -*-

import socket
import threading
import Queue
import time
import json
import psutil
import subprocess


class Client:
    def getconfig(self):
        self.config = json.loads((open("client.cfg", "r")).read())
        self.code = self.config["code"]
        self.connection_server = (self.config["server"], self.config["port"])
        self.production_line = Queue.Queue(10)
        self.delivery_line = Queue.Queue(1)
        self.connected = False

    def start_th(self, target, args = (), daemon = False):
        th = threading.Thread(target = target, args = args)
        th.setDaemon(daemon)
        th.start()
        return th

    # def get_messages(self):
    #     self.warehouse.get(block = True, timeout = None)

    def connection(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(self.connection_server)

    def listen(self):
        message = self.socket_client.recv(10240)
        return message

    def send(self, message):
        self.socket_client.send(message)

    # def listen(self):
    #     while True:
    #         message = self.socket_client.recv(1024)
    #         return message

    def cmd(self, cmmd):
        temp = subprocess.Popen(cmmd, stdout = subprocess.PIPE, shell = True)
        out = temp.stdout.read()
        out = self.fixchar(out)
        return out

    def fixchar(self, input):
        out = input.replace("\r", "")
        out = out.replace("\n", "")
        out = out.replace("\t", "")

        # out = out.replace("", "")

        out = out.replace("\xc7\xf1", "ñ")
        out = out.replace("\xc7\xfc", "ó")
        out = out.replace("\xc7\xfd", "ò")
        out = out.replace("\xc3\xb3", "ó")

        out = out.replace("\xa2", "ó")
        out = out.replace("\x85", "à")
        out = out.replace("\x88", "ê")
        out = out.replace("\xa4", "ñ")

        out = out.decode("utf-8", "ignore")

        return out

    def clock(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def qinfo(self):
        def hddusage():
            temp = psutil.disk_partitions()[0]
            if temp[0][0] == "C":
                temp = psutil.disk_usage(temp[0])[3]
            else:
                temp = 0
            return temp

        cpu = psutil.cpu_percent(interval = 5)
        ram = psutil.virtual_memory()[2]
        hdd = hddusage()
        return {"<QINFO>": [[self.clock(), cpu, ram, hdd]], "code": self.code}

    def info(self):
        data = self.cmd("wmic2json.cmd")
        data = json.loads(data)
        return {"<INFO>": [[self.clock(), data]], "code": self.code}

    def decode(self, message):  # REPLACE!!
        message = json.dumps(message)
        return message

    def disconnect(self):
        self.connected = False
        self.socket_client.close()
