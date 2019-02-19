import select, socket, queue
BUFFER_SIZE = 1024


class WebHandler:

    def __init__(self,
                 handlers):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind(('', 50000))
        self.server.listen(15)
        self.inputs = [self.server]
        self.outputs = []
        self.message_queues = {}
        self.handlers = handlers

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
                self.clear(s)

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
            cmd = s.recv(3)
            if cmd:
                cmddec = cmd.decode('utf-8')
                if cmddec == 'END':
                    self.clear(s)
                    return
                print(cmddec)
                data = self.receive(s)
                self.message_queues[s].put(self.handlers[cmddec](data))
                if s not in self.outputs:
                    self.outputs.append(s)
            else:
                self.clear(s)

    def accept(self,
               s):
        connection, client_address = s.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        self.message_queues[connection] = queue.Queue()

    def clear(self,
              s):
        self.inputs.remove(s)
        if s in self.outputs:
            self.outputs.remove(s)
        s.close()
        del self.message_queues[s]

    def receive(self,
                s):
        data = s.recv(BUFFER_SIZE)
        while True:
            try:
                rec = s.recv(BUFFER_SIZE)  # are we 100% certain that this works in every condition?
                if rec is None:
                    print(rec)
                    break
            except BlockingIOError:
                break
            data += rec
        return data
