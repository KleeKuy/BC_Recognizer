import socket
from time import sleep
import logging


class WebHandler:

    def __init__(self,
                 port,
                 ip,
                 handlers=None):
        self._conn = None
        self._addr = None
        self._ip = ip
        self._port = port
        self._handlers = handlers

    def listen(self):
        BUFFER_SIZE = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self._ip, self._port))
        s.listen(1)
        s.setblocking(0)
        while True:
            try:
                self._conn, self._addr = s.accept()
            except BlockingIOError:
                sleep(1)
                print("blockingioerror")
                continue
            break

        logging.info('Connection address:', self._addr) #TODO add logging? logging to file?

        cmd = self._conn.recv(3)
        cmddec = cmd.decode('utf-8')
        print(cmddec)
        data = self._conn.recv(BUFFER_SIZE)

        while True:
            try:
                rec = self._conn.recv(BUFFER_SIZE)  # are we 100% certain that this works in every condition?
            except BlockingIOError:
                break
            data += rec

        datadec = data.decode('utf-8')
        response = self._handlers[cmddec](datadec).encode('utf-8')
        self._conn.send(response)
        self._conn.close()
