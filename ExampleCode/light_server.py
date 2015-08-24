#!/usr/bin/env python
#!coding=utf-8

import logging
import time
import os
import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer
#from car import Car
import threading
import signal
import Adafruit_BBIO.GPIO as GPIO
import grove_sound_sensor


RELAY = "P9_22"            # GPIO P9_22
GPIO.setup(RELAY, GPIO.OUT)

SoundLimen = 0.1
Flag       = 0
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

#HTTP_PORT = 8000
HTTP_PORT = 8000
WEBSOCKET_PORT = 8001

class CommandWebsocket(WebSocket):

    def handleMessage(self):
        print self.data, 'from', self.address
        if self.data is None:
            self.data = ''
            print 'none'
        elif self.data == '1':
            print 'Turn On'
            Flag = 1
            GPIO.output(RELAY, GPIO.HIGH)
            #car.forward()
        elif self.data == '0':
            print 'Turn Off'
            Flag = 0
            GPIO.output(RELAY, GPIO.LOW)
            #car.backward()

        try:
            self.sendMessage(str(self.data))
        except Exception as n:
            print n

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        #car.stop()
        print self.address, 'closed'

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/www')
    SocketServer.TCPServer.allow_reuse_address = True
    httpserver = SocketServer.TCPServer(
        ('', HTTP_PORT), SimpleHTTPRequestHandler)
    print('car http server port: %d' % HTTP_PORT)
    httpd = threading.Thread(target=httpserver.serve_forever)
    httpd.start()
    websocket = SimpleWebSocketServer('', WEBSOCKET_PORT, CommandWebsocket)

    def close_sig_handler(signal, frame):
        #car.quit()
        httpserver.shutdown()
        httpd.join()
        websocket.close()

        print('quit')
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)
    while True:
        websocket.serveforever()
        if grove_sound_sensor.read_sound_sensor_values() >= SoundLimen:
            if Flag == 0:
                Flag = 1
                print 'Turn On'
                GPIO.output(RELAY, GPIO.HIGH)
            elif Flag == 1:
                Flag = 0
                print 'Turn Off'
                GPIO.output(RELAY, GPIO.LOW)
                
            
