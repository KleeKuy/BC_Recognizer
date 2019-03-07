from Processing.DataExtractor import DataExtractor
from Processing.PostProcess import PostProcess
from Connection.WebHandler_unittest import WebServetTest
from Connection.InputHandler import InputHandler
from Connection.WebHandler import WebHandler
from Connection.InputHandler_unittest import InputTest
from threading import Thread
from time import sleep
import socket
from Connection.HttpHandler_unittest import WebServetHttpTest


def begin():

    ex = DataExtractor("w4a.jpg")

#    ex.showrois()
    post = PostProcess()
    post.getsub(string=ex.extract(threshtype="otsu"))

    return


def main():
    #unittests()

    #app_test()
    #http_test = WebServetHttpTest()
    #http_test.test()
    httptets = WebServetHttpTest()
    httptets.test()


def init_conn():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def unittests():
   # unittestdb = DatabaseTest()
   # unittestdb.run_all()
    unittestweb = WebServetTest()
    unittestweb.run_all()
    unittestinpt = InputTest()
    unittestinpt.run_all()


def app_test():
    inpt = InputHandler()
    web = WebHandler(inpt.get_handlers())
    #client = Thread(target=send)
    #client.start()
    web.run()


def send():
    example = "NAME:WONSZ2/PASSWORD:RZECZNY/EMAIL:JESTNIEBEZPIECZNY/DUDUDUDU:DUDUDUDU".encode('utf-8')
    example2 = "NAME:WONSZ2/PASSWORD:RZECZNY".encode('utf-8')
    sleep(2)
    cmd = 'ADU'.encode('utf-8')
    port = 50000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    s.send('ADU'.encode('utf-8'))
    s.send(example)
    rec = s.recv(1)
    print(rec.decode('utf-8'))
   # msg = rec.decode('utf-8')

    s.send('VER'.encode('utf-8'))
    s.send(example2)
    rec = s.recv(1)
    print(rec.decode('utf-8'))

    s.send('IMG'.encode('utf-8'))
    s.send(example2)
    rec = s.recv(1)
    print(rec.decode('utf-8'))

    s.send('END'.encode('utf-8'))
    s.close()


if __name__ == "__main__":
    main()



