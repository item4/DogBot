# -*- coding: utf-8 -*-

__all__ = ['DogBotObject']

import cmd
import os
import random
import re
import select
import sys
import traceback
import time

from system.command import *
from system.error import *
from system.line import *
from threading import Thread

class DogBotObject(object):
    def __init__(self, system, server, connect, encoding, channels):
        self.system = system
        self.server = server
        self.con = connect
        self.encoding = encoding
        self.channels = channels

        self.running = True
        self.restart = False
        self.login = {}
        self.db = {}
        self.start_time = 0.
        self.handler = {}

        self.nick = system.config['nick']

        self.cmd = DogBotCommand(self)

        while self.system.running and (self.running or self.restart):
            try:
                self._start()
                self._run()
            except DogBotError as e:
                if e == 'QUIT':
                    break
            except Exception as e:
                with open('exception.log','a') as f:
                    exc_type, exc_value, exc_traceback = sys.exc_info()

                    f.write('Uncatched Exception at ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
                    traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
                    f.write('\n\n')
                raise e
            finally:
                self._stop()

    def _start(self):
        self.running = True
        self.restart = False
        self.start_time = time.time()

        self.con.connect()
        self.login.clear()
        self.db.clear()

        self.db['server']={}
        self.db['channel']={}
        self.db['busy']={}


    def _run(self):
        self.con.send(u'NICK %s' % self.nick)
        self.con.send(u'USER dog %s dog : dog' % self.con.host)

        temp = ''
        lines = []

        while self.system.running and self.running:
            recv = ''
            while not recv:
                try:
                    ready = select.select([self.con.connect], [], [], 1) # http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
                    if ready[0]:
                        recv = self.con.recv()
                except socket.timeout:
                    pass
                except select.error:
                    pass
                except socket.error:
                    return
                """else:
                    if not recv:
                        pass"""

            recv = temp + recv
            #lines = recv.splitlines()
            lines = recv.split('\n')

            for line in lines[:-1]:
                line = line.rstrip("\r\n")
                self.parse(line)

            temp = lines[-1]

        return

    def _stop(self):
        self.con.close()

    def parse(self, msg):
        temp = u'[%s]<< %s' % (time.strftime('%H:%M:%S'),msg)
        print temp.encode('cp949','replace')

        if msg.startswith(u'PING'):
            if msg[5] == ':':
                self.con.send(u'PONG %s' % msg[6:])
            else:
                self.con.send(u'PONG %s' % msg[5:])
        elif msg.startswith(u'ERROR'):
            if self.running:
                self.restart = True
        else:
            line = DogBotLine(msg,self.login)
            #print(repr(line.message))
            handler = self.handler.get(line.type.upper())
            if handler:
                for k, v in handler.iteritems():
                    try:
                        res = v(self, line)
                    except Exception as e:
                        self.con.query(
                            'PRIVMSG',
                            line.target,
                            u'[%s] %s: %s' % (k, e.__class__.__name__, e)
                        )
                    if res == cmd.STOP:
                        return
            try:
                func = getattr(self,'on_%s' % line.type.upper())
            except:
                pass
            else:
                func(line)

    def add_handler(self, event, name, func):
        event = event.upper()
        if event not in self.handler:
            self.handler[event] = {}

        self.handler[event][name] = func

    def del_handler(self, event, name):
        event = event.upper()
        if event not in self.handler or name not in self.handler[event]:
            return
        del self.handler[event][name]

    def del_handler_all(self):
        self.handler.clear()


    def on_001(self, line): # 서버 접속
        self.con.send(u'MODE %s +x' % self.nick)

    def on_005(self, line): # server options
        option = line.target.split(' ')[1:]
        for x in option:
            if '=' in x:
                key, value = x.split('=',1)
            else:
                key = x
                value = 1
            self.db['server'][key] = value

    def on_332(self, line): # channel topic
        _, channel = line.target.split(' ',1)

        if channel not in self.db['channel']:
            self.db['channel'][channel] = {}

        self.db['channel'][channel]['topic'] = line.message

    def on_333(self, line): # channel topic setter and time
        _, channel, setter, settime  = line.message.split(' ',3)

        if channel not in self.db['channel']:
            self.db['channel'][channel] = {}

        self.db['channel'][channel]['topic_setter'] = setter
        self.db['channel'][channel]['topic_time'] = settime

    def on_353(self, line): # channel member
        _, _, channel = line.target.split(' ',2)
        prefix = list(self.db['server']['STATUSMSG'])

        if channel not in self.db['channel']:
            self.db['channel'][channel] = {}

        if 'member' not in self.db['channel'][channel]:
            self.db['channel'][channel]['member'] = {}

        member = line.message.split(' ')

        for x in member:
            if not x:
                continue
            if x[0] in prefix:
                pre = set(x[0])
                nick = x[1:]
            else:
                pre = set()
                nick = x

            self.db['channel'][channel]['member'][nick] = pre

    def on_396(self, line): # motd 끝
        if self.system.config['nickserv'][self.server]['login']:
            self.con.send(self.system.config['nickserv'][self.server]['login'] % self.nick)

        for x in self.channels:
            self.con.query(
                'JOIN',
                x
            )

    def on_433(self, line): # nick 중복
        self.con.send(u'NICK %s．%d' % (self.nick,random.randint(1,99)))
        if self.system.config['nickserv'][self.server]['kick']:
            self.con.send(self.system.config['nickserv'][self.server]['kick'] % self.nick)
            self.con.send(u'NICK %s' % self.nick)

    def on_JOIN(self, line):
        if line.message in self.db['channel']:
            self.db['channel'][line.message]['member'][line.nick] = ''

    def on_MODE(self, line):
        temp = re.match('\((.+?)\)(.+$)', self.db['server']['PREFIX'])

        mode_str = list(temp.group(1))
        prefix_str = list(temp.group(2))

        chunk = line.message.split(' ')

        if len(chunk) == 3 and chunk[0][0] == '#':
            channel, mode, temp = chunk
            flag = ''
            i = 0
            nicks = temp.split()
            for m in list(mode):
                if m in '+-':
                    flag = m
                else:
                    try:
                        if flag == '+':
                            self.db['channel'][channel][nicks[i]] = self.db['channel'][channel][nicks[i]] | set(prefix_str[mode_str.index(m)])
                        else:
                            self.db['channel'][channel][nicks[i]] = self.db['channel'][channel][nicks[i]] - set(prefix_str[mode_str.index(m)])
                    except:
                        pass
                    i += 1

    def on_NICK(self, line): # change nick
        temp = self.db['busy'].get(line.nick)

        if temp:
            del self.db['busy'][line.nick]
            self.db['busy'][line.message] = temp


        for chan in self.db['channel']:
            temp = self.db['channel'][chan]['member'].get(line.nick)

            if temp:
                del self.db['channel'][chan]['member'][line.nick]
                self.db['channel'][chan]['member'][line.message] = temp

    def on_KICK(self, line):
        chan, nick = line.target.split(' ')

        if nick == self.nick:
            self.db['channel'][chan]['member'].clear()

            if chan in self.channels:
                self.con.query(
                    'JOIN',
                    chan
                )
                time.sleep(.1)
                self.con.query(
                    'PRIVMSG',
                    chan,
                    u'깨갱'
                )
        else:
            del self.db['channel'][chan]['member'][nick]

    def on_PART(self, line):
        if line.nick == self.nick:
            self.db['channel'][line.target].clear()
        else:
            del self.db['channel'][line.target]['member'][line.nick]

    def on_PRIVMSG(self, line):
        if line.message.startswith(self.nick):
            self.con.query(
                u'PRIVMSG',
                line.target,
                u'멍멍! %s는 item4가 키우는 파이썬 봇입니다. 명령어 : ?list | https://github.com/item4/DogBot' % self.nick
            )
        elif re.match(ur'(멍+!*\s*)+$',line.message):
            self.con.query(
                u'PRIVMSG',
                line.target,
                line.message,
            )
        elif line.message.startswith('/') or line.message.startswith('?'):
            Thread(
                target = self.cmd.run,
                kwargs = {'bot':self,'line':line},
            ).start()

    def on_QUIT(self, line):
        for chan in self.db['channel']:
            if line.nick in self.db['channel'][chan]['member']:
                del self.db['channel'][chan]['member'][line.nick]

    def on_TOPIC(self, line): # set topic
        self.db['channel'][line.target]['topic'] = line.message
        self.db['channel'][line.target]['topic_setter'] = line.mask


def main():
    pass

if __name__ == '__main__':
    main()
