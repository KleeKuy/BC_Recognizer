from Processing.DataExtractor import DataExtractor
from Processing.PostProcess import PostProcess
from Connection.WebHandler_unittest import WebServetTest
from Connection.InputHandler import InputHandler
from Connection.WebHandler import WebHandler
from Connection.InputHandler_unittest import InputTest
from http.server import HTTPServer
from Connection.HttpHandler import WebHandlerHttp
from Database.DataBase_unittest import DatabaseTest
from Processing.Processing_test import Tester
from time import sleep
import socket
from Connection.HttpHandler_unittest import WebServetHttpTest
from Database.sqlite_test import sqlite_test


def test_processing():
    Tester().test()
    return


def main():


    #unittests()

    #app_test()

   # test_processing()
   run_app()


def run_app():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, WebHandlerHttp)
    print("start")
    httpd.serve_forever()


def unittests():
    unittestdb = DatabaseTest()
    unittestdb.run_all()
    #unittestweb = WebServetTest()
    #unittestweb.run_all()
   # unittestinpt = InputTest()
   # unittestinpt.run_all()
   # httptets = WebServetHttpTest()
   # httptets.run_all()
    print("Somehow all tests passed :O!")


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



