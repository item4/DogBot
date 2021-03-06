# -*- coding: utf-8 -*-

__all__ = ['DogBotConnection']

import socket
import time
from threading import Thread
from Queue import Queue

class DogBotConnection(object):
    def __init__(self, system, host, port, encoding):
        self.system = system
        self.host = host
        self.port = port
        self.encoding = encoding
        self.queue = None


    def connect(self):
        self.running = True
        self.queue = Queue()
        self.connect = socket.socket()
        self.connect.settimeout(121)

        self.connect.connect((self.host, self.port))
        Thread(target=self.run).start()


    def recv(self):
        recv = self.connect.recv(4096).decode(self.encoding, 'replace')
        return recv


    def send(self, msg):
        temp = u'[%s]>> %s' % (time.strftime('%H:%M:%S'), msg)
        print temp.encode(self.system.encoding,'replace')
        msg += u"\r\n"
        self.connect.send(msg.encode(self.encoding, 'replace'))


    def append(self, msg):
        try:
            self.queue.put((msg, self.queue.qsize() / 10))
        except AttributeError:
            pass


    def run(self):
        while self.running:
            msg,sleep = self.queue.get()
            if msg is None:
                break
            self.send(msg)
            time.sleep(.1+sleep)

        if msg and not self.system.running:
            self.connect.send('QUIT :' + self.system.exit_reason)


    def query(self, msg_type, target=None, message=None):
        msg = msg_type
        if target:
            if message:
                msg += ' ' + target
            else:
                msg += ' :' + target

        if message:
            while len(message) > 200:
                self.append(msg + ' :' + message[:200])
                message = message[200:]
            else:
                self.append(msg + ' :' + message)
        else:
            self.append(msg)


    def close(self):
        self.running = False
        try:
            self.connect.close()
        except:
            pass
        del self.connect
        del self.queue
