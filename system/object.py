# -*- coding: utf-8 -*-

__all__ = ['DogBotObject']

import os
import re
import select
import time

from system.command import *
from system.error import *
from system.line import *
from threading import Thread

class DogBotObject:
    def __init__(self, system, connect, encoding, channels):
        self.system = system
        self.con = connect
        self.encoding = encoding
        self.channels = channels

        self.running = True
        self.restart = False
        self.login = {}
        self.db = {}
        self.start_time = 0.

        self.nick = u'멍멍이'

        self.cmd = DogBotCommand()

        while self.system.running and (self.running or self.restart):
            try:
                self._start()
                self._run()
            except DogBotError as e:
                if e == 'QUIT':
                    break
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
            try:
                func = getattr(self,'on_%s' % line.type.upper())
            except:
                pass
            else:
                func(line)

    def on_001(self, line): # 서버 접속
        self.con.send(u'MODE %s +x' % self.nick)

    def on_433(self, line): # nick 중복
        self.nick = u'멍멍이%d호' % random.randint(1,9999)
        self.con.send(u'NICK %s' % self.nick)

    def on_330(self, line): # whois login
        _, nick, id = line.target.split(' ')

        """if id in self.login.values():
            for k,v in self.login.items():
                if v == id:
                    del self.login[k]"""

        self.login[nick] = id

        self.con.query(
            u'NOTICE',
            nick,
            u'로그인 되었습니다.'
        )

    def on_QUIT(self, line):
        if line.nick in self.login:
            del self.login[line.nick]

        if line.nick in self.db['busy']:
            del self.db['busy'][line.nick]

        for chan in self.db['channel']:
            if line.nick in self.db['channel'][chan]['member']:
                del self.db['channel'][chan]['member'][line.nick]

    def on_PART(self, line):
        if line.nick == self.nick:
            self.db['channel'][line.target].clear()
        else:
            del self.db['channel'][line.target]['member'][line.nick]

    def on_JOIN(self, line):
        if line.message in self.db['channel']:
            self.db['channel'][line.message]['member'][line.nick] = ''

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


    def on_NICK(self, line): # change nick
        temp = self.login.get(line.nick)

        if temp:
            del self.login[line.nick]
            self.login[line.message] = temp


        temp = self.db['busy'].get(line.nick)

        if temp:
            del self.db['busy'][line.nick]
            self.db['busy'][line.message] = temp


        for chan in self.db['channel']:
            temp = self.db['channel'][chan]['member'].get(line.nick)

            if temp:
                del self.db['channel'][chan]['member'][line.nick]
                self.db['channel'][chan]['member'][line.message] = temp



    def on_396(self, line): # motd 끝
        for x in self.channels:
            self.con.query(
                'JOIN',
                x
            )

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
                pre = x[0]
                nick = x[1:]
            else:
                pre = ''
                nick = x

            self.db['channel'][channel]['member'][nick] = pre

    def on_TOPIC(self, line): # set topic
        self.db['channel'][line.target]['topic'] = line.message
        self.db['channel'][line.target]['topic_setter'] = line.mask

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
        else:
            for x in self.db['busy'].keys():
                reason, busytime = self.db['busy'].get(x)
                busytime = time.time() - busytime

                if line.nick == x:
                    self.con.query(
                        u'PRIVMSG',
                        line.target,
                        u'%s, 부재를 해지합니다. (%s 동안 부재였음.)' % (x,read_time(busytime))
                    )
                    del self.db['busy'][x]

                elif line.message.startswith(x) and x in self.db['channel'][line.target]['member']:

                    self.con.query(
                        u'PRIVMSG',
                        line.target,
                        u'%s, %s님은 %s 전부터 부재중입니다. (이유: %s)' % (line.nick,x,read_time(busytime),reason)
                    )

def main():
    pass

if __name__ == '__main__':
    main()
