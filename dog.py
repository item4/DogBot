# -*- coding:utf-8 -*-

import os
import sys
import socket
import time
import re
import string
import random
import select
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
    def __init__(self):
        self.cmdlist = {}
        self.syscmd = ['load','reload','list']
        self.reload()

    def reload(self, cmdname=None):
        if cmdname is None:
            self.cmdlist.clear()
            os.chdir('c:/py/DogBot/')
            cmdlist = os.listdir('./cmd/')
            res = 0
            total = 0
            for x in cmdlist:
                if not x.endswith('.py') or x.startswith('__init__'):
                    continue
                x = x.replace('.py', '')
                res += self._load(x)
                total += 1
            return res,total
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
                return self._load(cmdname)
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
        try:
            if temp:
                reload(temp)
            else:
                __import__(modname)
        except:
            return 0
        else:
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
            return 1

    def run(self, bot, line):
        temp = line.message.split(' ', 1)
        cmd = temp[0][1:]
        args = None
        if len(temp) == 2:
            args = temp[1]

        if cmd in self.cmdlist:
            try:
                self.cmdlist[cmd](bot, line, args)
            except Exception as e:
                try:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s: %s' % (e.__class__.__name__,e)
                    )
                except:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s: %s' % (e.__class__.__name__,e.decode('utf8'))
                    )
        elif cmd in self.syscmd:
            func = getattr(self,'cmd_%s' % cmd)
            func(bot,line,args)

    def cmd_load(self, bot, line, args):
        if line.login != 'item4':
            return
        if not args:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'뭘?'
            )
        else:
            try:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 로드 시작' % args
                )
                self.load(args)
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 로드 실패 - %s: %s' % (args,e.__class__.__name__,e)
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 로드 성공' % args
                )
    def cmd_reload(self, bot, line, args):
        if line.login != 'item4':
            return
        if args:
            try:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 리로드 시작' % args
                )
                self.reload(args)
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 리로드 실패 - %s: %s' % (args,e.__class__.__name__,e)
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 리로드 성공' % args
                )
        else:
            try:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'모든 명령어 리로드 시작'
                )
                success,total = self.reload()
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'모든 명령어 리로드 실패 - %s: %s' % (e.__class__.__name__,e)
                )
            else:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'총 %d개의 모듈중 %d개 모듈 로딩 성공, 총합 %d개의 명령어 리로드됨' % (total,success,len(self.cmdlist))
                )

    def cmd_list(self, bot, line, args):
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'총 %d개의 명령어와 %d개의 시스템 명령어가 있습니다' % (len(self.cmdlist),len(self.syscmd))
        )
        bot.con.query(
            'PRIVMSG',
            line.target,
            ', '.join(sorted(self.cmdlist.keys()+self.syscmd))
        )







class DogBotObject:
    def __init__(self, connect):
        self.running = True
        self.con = connect
        self.nick = u'멍멍이'
        self.login = {}
        self.start = 0.

        self.cmd = DogBotCommand()
        while True:
            self._start()
            try:
                self._run()
            finally:
                self._stop()

    def _start(self):
        self.con.connect()
        self.restart = False
        self.login.clear()
        self.start = time.time()

    def _run(self):
        self.con.send(u'NICK %s' % self.nick)
        self.con.send(u'USER dog %s dog : dog' % self.con.host)

        temp = ''
        lines = []

        while self.running and not self.restart:
            recv = ''
            while not recv:
                try:
                    ready = select.select([self.con.connect], [], [], 1) # http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
                    if ready[0]:
                        recv = self.con.recv()
                except socket.timeout:
                    pass
                except select.error as e:
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

    def parse(self,msg):
        temp = u'[%s]<< %s' % (time.strftime('%H:%M:%S'),msg)
        print temp.encode('cp949','replace')

        if msg.startswith(u'PING'):
            if msg[5] == ':':
                self.con.send(u'PONG %s' % msg[6:])
            else:
                self.con.send(u'PONG %s' % msg[5:])
        elif msg.startswith(u'ERROR'):
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

    def on_001(self,line): # 서버 접속
        self.con.send(u'MODE %s +x' % self.nick)

    def on_433(self,line): # nick 중복
        self.nick = u'멍멍이%d호' % random.randint(1,9999)
        self.con.send(u'NICK %s' % self.nick)

    def on_330(self,line):
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

    def on_QUIT(self,line):
        if line.nick in self.login:
            del self.login[line.nick]

    def on_NICK(self,line):
        print line
        temp = self.login.get(line.nick)

        if temp:
            del self.login[line.nick]
            self.login[line.message]=temp

    def on_396(self,line): #motd 끝
        self.con.send(u'JOIN #item4')

    def on_PRIVMSG(self,line):
        if line.message == self.nick:
            self.con.query(
                u'PRIVMSG',
                line.target,
                u'멍멍! %s는 item4가 키우는 파이썬 봇입니다.' % self.nick
            )
        elif re.match(ur'멍+!*$',line.message):
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

class DogBotLine:
    __slots__ = "nick", "ident", "ip", "server", "type", "target", "message", "login"
    nick = ident = ip = server = type = target = message = login = None

    def __init__(self, msg, login):
        if msg[1:].find(':') > 0:
            temp, message = msg[1:].split(':',1)

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
        else:
            temp, self.type, self.message = msg[1:].split(' ',2)
            if temp.find('!') > 0:
                try:
                    self.nick,t=temp.split('!',1)
                except:
                    print temp
                self.ident, self.ip = t.split('@',1)
            else:
                self.server = temp

        self.login = login.get(self.nick)

    def __repr__(self):
        temp = [self.nick,self.ident,self.ip,self.server,self.type,self.target,self.message,self.login]
        for i in xrange(len(temp)):
            if temp[i] is not None:
                temp[i] = temp[i].encode('utf8')

        format = "'nick':{!r},'ident':{!r},'ip':{!r},'server':{!r},"
        format += "type:{!r},target:{!r},message:{!r},login:{!r}"
        return '<DogBotLine>{' + format.format(*temp) + '}'


class DogBotConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.queue = None

    def connect(self):
        self.running = True
        self.queue = Queue()
        self.connect = socket.socket()
        #self.connect.settimeout(1)

        self.connect.connect((self.host, self.port))
        #self.connect.setblocking(0)
        Thread(target=self.run).start()

    def recv(self):
        recv = self.connect.recv(4096).decode('utf8', 'replace')
        return recv

    def send(self, msg):
        temp = u'[%s]>> %s' % (time.strftime('%H:%M:%S'), msg)
        print temp.encode('cp949','replace')
        msg += u"\r\n"
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
        try:
            self.connect.close()
        except:
            pass
        del self.connect
        del self.queue

class DogBotError(Exception):
    pass

def main():
    dog = DogBot()
    dog.add_connect(u'kanade.irc.ozinger.org', 6667)
    dog.start()

if __name__ == '__main__':
    main()