# -*- coding: utf-8 -*-

import client
import time


class MethodClient(client.Client):

    def __init__(self):
        self.vars()


    def routine1(self):
        """out: 'kraken.fintra.co' : [[192.168.0.1], 14.5, 65.4, 48.3]"""
        while True:
            try:
                message = self.qinfo()
                message = self.formatout(message)
                self.connect()
                self.send(message)
                self.disconnect()
            except:
                break

    def connect(self):
        while True:
            try:
                self.connection()
                break
            except:
                time.sleep(1)
                pass




    def communication(self,action,message):
        """action: ["<send>": send a message; "<listen>: listen for admin"]"""""

        if action == "<send>":

            th1 = threading.Thread(target = self.send_child, args = (message,))
            th1.setDaemon(True)
            th1.start()

        # th1 = threading.Thread(target = self.send_child, name = "th1")
        # th1.setDaemon(True)
        # th1.start()
        #
        # th2 = threading.Thread(target = self.listen_child, name = "th2")
        # th2.setDaemon(True)
        # th2.start()

        self.hold_connection.get(block = True, timeout = None)

    def send_child(self,message):
        while True:
            try:
                self.send(message)
            except:
                self.close()

    def listen_child(self):
        while True:
            try:
                message = self.listen()
                self.process(message)
            except:
                self.close()
                break
