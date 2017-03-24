# -*- coding: utf-8 -*-

import client
import sys
import time
import threading
import logging


class MethodClient(client.Client):

    def __init__(self):
        self.getconfig()

        logging.basicConfig(
            filename = 'client.log',
            level = logging.DEBUG,
            format = '%(asctime)s - %(name)-13s: %(levelname)-8s - %(message)s')
        logging.info(self.code)

    def routine1(self):
        """QINFO"""
        logger = logging.getLogger("routine1")
        timeout = 60 #burn

        self.start_th(self.factory)
        self.start_th(self.warehouse)
        self.start_th(self.connect)

    def factory(self):
        logger = logging.getLogger("factory")
        # lock = threading.Lock()
        while True:
            try:
                package = self.qinfo()
                logger.debug("qinfo generado")
                self.production_line.put(package, block = True, timeout = None)
            except Exception as err:
                logger.warning(err)
                pass

    def warehouse(self):
        logger = logging.getLogger("warehouse")
        box = {}
        while True:
            try:
                package = self.production_line.get(block = True, timeout = None)
                #agregar a la caja
                if not box:
                    box = package
                    logger.debug("nueva caja creada")
                elif "<QINFO>" in box:
                    box["<QINFO>"].append(package["<QINFO>"][0])
                    logger.debug("qinfo añadido a caja")
                    # logger.info(box)
                elif "<INFO>" in box:
                    box["<INFO>"].append(package["<INFO>"][0])
                    logger.debug("info añadido a caja")
                    # logger.info(box)
                else:
                    for i in package:
                        box[i] = package[i]
                #caja
                print box

                closedbox = self.decode(box)
                self.send(closedbox)
                box = {}
                self.disconnect()

            except Exception as err:
                # logger.warning(err)
                pass

    def routine2(self):
        """INFO"""
        logger = logging.getLogger("routine2")
        while True:
            try:
                message = self.info()
                logger.debug("info generado")
                message = self.decode(message)
                logger.debug("info decodificado")
                self.connect()
                logger.debug("conectado a servidor")
                self.send(message)
                logger.debug("mensaje enviado")
                self.disconnect()
                logger.debug("desconectado del servidor")
            except Exception as err:
                logger.warning(err)
                pass
            time.sleep(5)

    def connect(self, retry = 10, retrytime = 3, timeout = 60):
        logger = logging.getLogger("connect")
        while True:
            count = 1
            while count <= retry:
                try:
                    logger.debug("intento " + str(count))
                    self.connection()
                    self.connected = True
                    logger.debug("conectado a servidor")
                    return 0
                except Exception as err:
                    # logger.warning(err)
                    time.sleep(retrytime)
                    count += 1
                    pass
            logger.debug("de nuevo en " + str(timeout))
            time.sleep(timeout)
