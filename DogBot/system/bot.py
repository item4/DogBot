# -*- coding: utf-8 -*-

__all__ = ['DogBot']

import json
import time

from threading import Thread

from DogBot.system.connection import *
from DogBot.system.object import *


class DogBot(object):
    def __init__(self):
        self.start_time = time.time()
        self._running = True
        self.exit_reason = ''
        self.encoding = 'cp949'  # system encoding
        self.dbname = 'DogBot.db'
        self.config = {}
        self.connections = []

    def add_connect(self, server, port, encoding, channels):
        connect = DogBotConnection(self, server, port, encoding)

        th = Thread(
            target=DogBotObject,
            name='DogObj#%s' % server,
            kwargs={'system': self,
                    'server': server,
                    'connect': connect,
                    'encoding': encoding,
                    'channels': channels},
        )

        self.connections.append({'server':server,'connect':connect,'thread':th})

    def start(self):
        for c in self.connections:
            c['thread'].start()

    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
                
                for server in self.config['server'].keys():
                    self.add_connect(server, self.config['server'][server]['port'], self.config['server'][server]['encoding'], self.config['server'][server]['channels'])
        except IOError:
            with open('config.json', 'w') as f:
                f.write('{"nick":"botname","server":'
                        '{"some server":{'
                        '"port":6667'
                        ',"encoding":"utf8"'
                        ',"channels":["#test"]'
                        ',"kick":"how to kick dup nick"'
                        ',"login":"how to login"}},"db":""}')
            exit


    @property
    def running(self):
        return self._running


    @running.setter
    def running(self, value):
        self._running = value
        if value == False:
            for c in self.connections:
                c['connect'].running = False
                c['connect'].query(None)