import select, socket, queue
from time import sleep
from Connection.CmdType import CmdType
import struct
BUFFER_SIZE = 1024


class WebHandler:

    def __init__(self,
                 handlers):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind(('', 5000))
        self.server.listen(15)
        self.inputs = [self.server]
        self.outputs = []
        self.message_queues = {}
        self.handlers = handlers
        self.db = {}

    def run(self):
        print('run start')
        while self.inputs:
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)
            for s in readable:
                self.read(s)
            for s in writable:
                self.write(s)
            for s in exceptional:
                ip, port = s.getsockname()
                self.clear(s, ip)

    def write(self,
              s):
        try:
            next_msg = self.message_queues[s].get_nowait()
        except queue.Empty:
            self.outputs.remove(s)
        except KeyError:
            print("socket already closed!")
        else:
            s.send(next_msg.encode('utf-8'))

    def read(self,
             s):
        if s is self.server:
            self.accept(s)
        else:
            ip, port = s.getsockname()
            print("ip in hndler is " + ip)
            try:
                cmd = s.recv(3)
            except ConnectionResetError:
                print("klient niespodziwanie zakonczyl polaczenie!")
                self.clear(s, ip)
                return
            if cmd:
                #cmddec = int(cmd)#int.from_bytes(cmd, byteorder='little')#.decode('utf-8')
                cmddec = cmd.decode('utf-8')
                print("received command is " + str(cmddec))
                if cmddec == CmdType.END.value:
                    self.clear(s, ip)
                    return
                data = self.receive(s)
                try:
                    self.message_queues[s].put(self.handlers[cmddec](data, ip))
                except KeyError:
                    self.clear(s, ip)
                    print("Cos ty mie przyslal???? " + str(cmddec))
                    return
                if s not in self.outputs:
                    self.outputs.append(s)
            else:
                self.clear(s, ip)

    def accept(self,
               s):
        connection, client_address = s.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        self.message_queues[connection] = queue.Queue()

    def clear(self,
              s,
              ip):
        print("clear")
        self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)
        s.close()
        del self.message_queues[s]
        self.handlers[CmdType.END.value](ip)

    def receive(self,
                s):
        tst = False
        data = b''
        while True:
            try:
                rec = s.recv(BUFFER_SIZE)  # are we 100% certain that this works in every condition?
       #         if rec is None and data is not None:
            #    print("received " + rec.decode('utf-8'))
       #             break
            except BlockingIOError:
                if tst is True:
                    break
                else:
                    tst = False
                print("sleepin")
                sleep(1)    #todo somehow set socket timeout instead of this
                tst = True
                continue
            data += rec
        return data
