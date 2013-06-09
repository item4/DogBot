# -*- coding: utf-8 -*-

__all__ = ['DogBot']

import json
import time
from threading import Thread
from system.connection import *
from system.object import *

class DogBot(object):
    def __init__(self):
        self.thread = []
        self.start_time = time.time()
        self.running = True
        self.exit_reason = ''
        self.encoding = 'cp949' #system encoding
        self.dbname = 'DogBot.db'
        self.config = {}

    def add_connect(self, server, port, encoding, channels):
        connect = DogBotConnection(self, server, port, encoding)

        th = Thread(
            target = DogBotObject,
            name = 'DogObj#%s' % server,
            kwargs = {'system':self, 'server':server, 'connect':connect, 'encoding':encoding, 'channels':channels},
        )

        self.thread.append(th)

    def start(self):
        for th in self.thread:
            th.start()

    def load_config(self):
        try:
            with open('config.json','r') as f:
                self.config = json.load(f)
        except IOError:
            with open('config.json','w') as f:
                f.write('{"nick":"botname","nickserv":{"some server":{"kick":"how to kick dup nick","login":"how to login"}},"db":""}')
            exit

def main():
    pass

if __name__ == '__main__':
    main()
