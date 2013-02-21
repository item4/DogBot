# -*- coding: utf-8 -*-

__all__ = ['DogBot']

import time
from threading import Thread
from system.connection import *
from system.object import *

class DogBot:
    def __init__(self):
        self.thread = []
        self.start_time = time.time()
        self.running = True
        self.exit_reason = ''
        self.encoding = 'cp949' #system encoding
        self.dbname = 'DogBot.db'

    def add_connect(self, server, port, encoding, channels):
        connect = DogBotConnection(self, server, port, encoding)

        th = Thread(
            target = DogBotObject,
            name = 'DogObj#%s' % server,
            kwargs = {'system':self, 'connect':connect, 'encoding':encoding, 'channels':channels},
        )

        self.thread.append(th)

    def start(self):
        for th in self.thread:
            th.start()

def main():
    pass

if __name__ == '__main__':
    main()
