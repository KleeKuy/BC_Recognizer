import socket
from time import sleep
import logging
BUFFER_SIZE = 1024


class WebHandler:

    def __init__(self,
                 port,
                 ip,
                 handlers):
        self._conn = None
        self._addr = None
        self._ip = ip
        self._port = port
        self._handlers = handlers

    def setup_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self._ip, self._port))
        s.setblocking(0)
        s.listen(1)
        while True:
            try:
                self._conn, self._addr = s.accept()
            except BlockingIOError:
                sleep(1)
                continue
            break
        logging.info('Connection address:', self._addr)  # TODO add logging? logging to file?

    def receive_command(self):
        while True:
            try:
                cmd = self._conn.recv(3)
            except BlockingIOError:
                sleep(1)
                continue
            break
        cmddec = cmd.decode('utf-8')
        logging.info('Command received :', cmddec)
        return cmddec

    def receive_data(self):
        data = self._conn.recv(BUFFER_SIZE)
        while True:
            try:
                rec = self._conn.recv(BUFFER_SIZE)  # are we 100% certain that this works in every condition?
            except BlockingIOError:
                break
            data += rec
        return data.decode('utf-8')

    def listen(self):
        while True:
            cmd = self.receive_command()
            if cmd == "END":
                break
            data = self.receive_data()
            try:
                response = self._handlers[cmd](data).encode('utf-8')
            except KeyError:
                self._conn.send("No such command")
                continue
            self._conn.send(response)
        self._conn.close()
