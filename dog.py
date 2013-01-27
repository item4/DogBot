# -*- coding:utf-8 -*-

import os
import sys
import socket
import time
import re
import string
from Queue import Queue
from threading import Thread

class DogBot:
    def __init__(self):
        self.thread = []

    def add_connect(self, server, port):
        connect = DogBotConnection(server, port)

        th = Thread(
            target = DogBotObject,
            name = 'DogObj#%s'%server,
            kwargs = {'connect':connect},
        )

        self.thread.append(th)

    def start(self):
        for th in self.thread:
            th.start()

class DogBotCommand:
    def __init__(self, con):
        self.con = con
        self.cmdlist = {}
        self.reload()
        self.syscmd = ['load','reload','list']

    def reload(self, cmdname=None):
        if cmdname is None:
            self.cmdlist.clear()
            os.chdir('c:/py/')
            cmdlist = os.listdir('./cmd/')
            for x in cmdlist:
                if not x.endswith('.py') or x.startswith('__init__'):
                    continue
                x = x.replace('.py', '')
                self._load(x)
        else:
            func = self.cmdlist.get(cmdname)
            if func:
                module = sys.modules[func._dogbot_modname]
                del self.cmdlist[cmdname]

                alias = list(module.alias)
                while alias:
                    aliasname = alias.pop()
                    if aliasname in self.cmdlist:
                        del self.cmdlist[aliasname]
                self._load(cmdname)
            else:
                raise DogBotError(u'로딩된적 없는 명령어')

    def load(self, cmdname=None):
        if cmdname not in self.cmdlist:
            self._load(cmdname)
        else:
            raise DogBotError(u'이미 로딩된 명령어')

    def _load(self, cmdname):
        modname = ".".join(["cmd", cmdname])
        print modname

        temp = sys.modules.get(modname)
        if temp:
            reload(temp)
        else:
            __import__(modname)

        module = sys.modules[modname]

        func = getattr(module, 'cmd_%s' % cmdname)
        func._dogbot_modname = modname
        self.cmdlist[cmdname] = func

        alias = list(module.alias)
        while alias:
            aliasname = alias.pop()
            #func = getattr(module,'cmd_%s' % aliasname)
            func = getattr(module,'cmd_%s' % cmdname)
            func._dogbot_modname = modname
            self.cmdlist[aliasname] = func

    def run(self, line):
        temp = line.message.split(' ', 1)
        cmd = temp[0][1:]
        args = None
        if len(temp) == 2:
            args = temp[1]

        if cmd in self.cmdlist:
            try:
                self.cmdlist[cmd](self.con, line, args)
            except Exception as e:
                self.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s: %s' % (e.__class__.__name__,e)
                )
        elif cmd=='load':
            if not args:
                self.con.query(
                    'PRIVMSG',
                    line.target,
                    u'뭘?'
                )
            else:
                try:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 로드 시작' % args
                    )
                    self.load(args)
                except Exception as e:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 로드 실패 - %s: %s' % (args,e.__class__.__name__,e)
                    )
                else:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 로드 성공' % args
                    )
        elif cmd=='reload':
            if args:
                try:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 리로드 시작' % args
                    )
                    self.reload(args)
                except Exception as e:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 리로드 실패 - %s: %s' % (args,e.__class__.__name__,e)
                    )
                else:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 리로드 성공' % args
                    )
            else:
                try:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'모든 명령어 리로드 시작'
                    )
                    self.reload()
                except Exception as e:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'모든 명령어 리로드 실패 - %s: %s' % (e.__class__.__name__,e)
                    )
                else:
                    self.con.query(
                        'PRIVMSG',
                        line.target,
                        u'총 %d개의 명령어 리로드 성공' % len(self.cmdlist)
                    )

        elif cmd=='list':
            self.con.query(
                'PRIVMSG',
                line.target,
                u'총 %d개의 명령어와 %d개의 시스템 명령어가 있습니다' % (len(self.cmdlist),len(self.syscmd))
            )
            self.con.query(
                'PRIVMSG',
                line.target,
                ', '.join(sorted(self.cmdlist.keys()+self.syscmd))
            )

        else:
            self.con.query(
                'PRIVMSG',
                line.target,
                u'%s는 없는 명령어' % (cmd)
            )



class DogBotObject:
    def __init__(self, connect):
        self.running = True
        self.con = connect
        self.nick = u'멍멍이'

        self.cmd = DogBotCommand(connect)
        while True:
            self._start()
            try:
                self._run()
            finally:
                self._stop()

    def _start(self):
        self.con.connect()
        self.restart = False

    def _run(self):
        self.con.send(u'NICK 멍멍이')
        self.con.send(u'USER dog %s dog : dog' % self.con.host)

        temp = ''
        lines = []

        while self.running and not self.restart:
            recv = self.con.recv()
            if not recv:
                break

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

    def parse(self,msg):
        print '[%s]<< %s' % (time.strftime('%H:%M:%S'),msg)

        if msg.startswith(u'PING'):
            self.con.send(u'PONG %s' % msg[6:])
        elif msg.startswith(u'ERROR'):
            self.restart = True
        else:
            line = DogBotLine(msg)
            #print(repr(line.message))

            if line.type == u'001':
                self.con.send(u'MODE %s +x' % self.nick)
            elif line.type == u'433':
                self.nick = u'으르릉'
                self.con.send(u'NICK %s' % self.nick)
            elif line.type == u'396':
                self.con.send(u'JOIN #item4')
            elif line.type == u'PRIVMSG' and line.message == u'멍멍이':
                self.con.query(
                    u'PRIVMSG',
                    line.target,
                    u'멍멍! 멍멍이는 item4가 키우는 파이썬 봇입니다.',
                )
            elif line.type==u'PRIVMSG' and re.match(ur'멍+!*$',line.message):
                self.con.query(
                    u'PRIVMSG',
                    line.target,
                    line.message,
                )
            elif line.type==u'PRIVMSG' and \
            (line.message.startswith('/') or line.message.startswith('?')):
                Thread(
                    target = self.cmd.run,
                    kwargs = {'line':line},
                ).start()

class DogBotLine:
    __slots__ = "nick", "ident", "ip", "server", "type", "target", "message"
    nick = ident = ip = server = type = target = message = None

    def __init__(self,msg):
        if msg[1:].find(':') > 0:
            temp, message = msg[1:].split(':',1)
        else:
            return

        self.message = message
        temp = temp.rstrip()
        temp = temp.split(' ', 2)
        if temp[0].find('!') > 0:
            try:
                self.nick,t=temp[0].split('!',1)
            except:
                print temp[0]
            self.ident, self.ip = t.split('@',1)
        else:
            self.server = temp[0]
        self.type = temp[1]

        if len(temp) == 3:
            self.target = temp[2]

class DogBotConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = Queue()

    def connect(self):
        self.running = True
        self.connect = socket.socket()
        self.connect.connect((self.host, self.port))
        Thread(target=self.run).start()

    def recv(self):
        recv = self.connect.recv(4096).decode('utf8', 'replace')
        return recv

    def send(self, msg):
        print '[%s]>> %s' % (time.strftime('%H:%M:%S'), msg)
        msg+='\r\n'
        self.connect.send(msg.encode('utf8', 'replace'))

    def append(self,msg):
        self.queue.put((msg, self.queue.qsize() / 10))

    def run(self):
        while self.running:
            while not self.queue.empty():
                msg,sleep=self.queue.get()
                self.send(msg)
                time.sleep(.1+sleep)

    def query(self, type, target=None, message=None):
        msg = type
        if target:
            msg += ' ' + target
        if message:
            msg += ' ' + message
        self.append(msg)

    def close(self):
        self.running = False
        self.connect.close()
        del self.connect

class DogBotError(Exception):
    pass

def main():
    dog = DogBot()
    dog.add_connect(u'kanade.irc.ozinger.org', 6667)
    dog.start()

if __name__ == '__main__':
    main()