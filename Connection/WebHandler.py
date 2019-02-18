import socket
from time import sleep
import logging
BUFFER_SIZE = 1024


class WebHandler:

    def __init__(self,
                 handlers):
        self._handlers = handlers

    def setup_connection(self,
                         port):
        setup = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        setup.bind(('', port))
        setup.setblocking(0)
        setup.listen(1)
        print("listening")
        while True:
            try:
                c, a = setup.accept()
            except BlockingIOError:
                sleep(1)
                continue
            break
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        print(port)
        c.send(port.to_bytes((port.bit_length() + 7) // 8, byteorder='big'))
        setup.close()
        sock.setblocking(0)
        sock.listen(1)
        while True:
            try:
                conn, addr = sock.accept()
            except BlockingIOError:
                sleep(1)
                continue
            break
        logging.info('Connection address:', addr)  # TODO add logging? logging to file?
        return sock, conn

    def receive_command(self,
                        conn):
        while True:
            try:
                cmd = conn.recv(3)
            except BlockingIOError:
                sleep(1)
                continue
            break
        cmddec = cmd.decode('utf-8')
        logging.info('Command received :', cmddec)
        return cmddec

    def receive_data(self,
                     conn):
        data = conn.recv(BUFFER_SIZE)
        while True:
            try:
                rec = conn.recv(BUFFER_SIZE)  # are we 100% certain that this works in every condition?
            except BlockingIOError:
                break
            data += rec
        return data.decode('utf-8')

    def listen(self,
               conn,
               sock):
        while True:
            cmd = self.receive_command(conn)
            if cmd == "END":
                break
            data = self.receive_data(conn)
            try:
                response = self._handlers[cmd](data).encode('utf-8')
            except KeyError:
                conn.send("No such command")
                continue
            conn.send(response)
        conn.close()
        sock.close()
