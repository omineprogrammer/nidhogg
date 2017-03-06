# -*- coding: utf-8 -*-

import client
import sys
import time
import logging


class MethodClient(client.Client):

    def __init__(self):
        self.getconfig()
        logging.basicConfig(
            filename = 'client.log',
            level = logging.DEBUG,
            format = '%(asctime)s - %(name)-15s - %(levelname)-8s - %(message)s')
        logging.info((self.clock(), self.id))

    def routine1(self):
        """QINFO"""
        logger = logging.getLogger("routine1")
        while True:
            try:
                message = self.qinfo()
                logger.debug("qinfo generado")
                message = self.decode(message)
                logger.debug("qinfo decodificado")
                self.connect()
                logger.debug("conectado a servidor")
                self.send(message)
                logger.debug("mensaje enviado")
                self.disconnect()
                logger.debug("desconectado del servidor")

            except Exception as err:
                logger.warning(err)
                break

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
                break
            time.sleep(5)


    def connect(self):
        logger = logging.getLogger("connect")
        while True:
            count = 1
            while count <= 10:
                try:
                    logger.debug("intento " + str(count))
                    self.connection()
                    return 0
                except Exception as err:
                    logger.warning(err)
                    time.sleep(3)
                    count += 1
                    pass
            logger.debug("de nuevo en 10\'")
            time.sleep(600)
