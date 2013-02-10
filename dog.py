# -*- coding:utf-8 -*-

import os
import sys
import socket
import time
import re
import string
import random
import select
import sqlite3
from Queue import Queue
from threading import Thread

def read_time(_time):
    _time = _time
    day, _time = divmod(_time,86400)
    hour, _time = divmod(_time,3600)
    minute, second = divmod(_time,60)
    temp = []
    if day:
        temp.append(str(int(day))+u'일')
    if hour:
        temp.append(str(int(hour))+u'시간')
    if minute:
        temp.append(str(int(minute))+u'분')
    if second or (not day and not hour and not minute):
        temp.append(str(int(second))+u'초')

    return ' '.join(temp)

class DogBot:
    def __init__(self):
        self.thread = []
        self.start_time = time.time()
        self.running = True
        self.exit_reason = ''

    def add_connect(self, server, port):
        connect = DogBotConnection(self, server, port)

        th = Thread(
            target = DogBotObject,
            name = 'DogObj#%s' % server,
            kwargs = {'system':self, 'connect':connect},
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
                        u'%s: ???' % (e.__class__.__name__)
                    )
        elif cmd in self.syscmd:
            func = getattr(self,'cmd_%s' % cmd)
            func(bot,line,args)

    def cmd_load(self, bot, line, args):
        if line.login != 'item4':
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 관리자만 사용가능한 명령어입니다.'
            )
            return
        if not args:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍?'
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
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 관리자만 사용가능한 명령어입니다.'
            )
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
    def __init__(self, system, connect):
        self.system = system
        self.con = connect

        self.running = True
        self.restart = False
        self.login = {}
        self.db = {}
        self.start_time = 0.

        self.nick = u'멍멍이'
        self.dbname = 'DogBot.db'

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
        del self.db['channel'][line.target]['member'][line.nick]

    def on_JOIN(self, line):
        if line.message in self.db['channel']:
            self.db['channel'][line.message]['member'][line.nick] = ''

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



    def on_396(self,line): # motd 끝
        self.con.send(u'JOIN #item4')

    def on_005(self,line): # server options
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

        if self.db['channel'][channel].get('member'):
            self.db['channel'][channel].clear()
        else:
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

class DogBotLine:
    __slots__ = "nick", "ident", "ip", "mask", "server", "type", "target", "message", "login"
    nick = ident = ip = mask = server = type = target = message = login = None

    def __init__(self, msg, login):
        if ':' in msg[1:]:
            temp, message = msg[1:].split(' :',1)

            self.message = message
            temp = temp.rstrip()
            temp = temp.split(' ', 2)
            if '!' in temp[0]:
                self.mask = temp[0]
                try:
                    self.nick, t = self.mask.split('!',1)
                except:
                    print self.mask
                self.ident, self.ip = t.split('@',1)
            else:
                self.server = temp[0]
            self.type = temp[1]

            if len(temp) == 3:
                self.target = temp[2]
        else:
            self.mask, self.type, self.message = msg[1:].split(' ',2)
            if '!' in self.mask:
                try:
                    self.nick, t = self.mask.split('!',1)
                except:
                    print mask
                self.ident, self.ip = t.split('@',1)
            else:
                self.server = self.mask
                self.mask = None

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
    def __init__(self, system, host, port):
        self.system = system
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
        try:
            self.queue.put((msg, self.queue.qsize() / 10))
        except AttributeError:
            pass

    def run(self):
        while self.running:
            if not self.system.running:
                self.com.send(u'QUIT %s' % self.system.exit_reason)
                break
            try:
                while not self.queue.empty():
                    msg,sleep = self.queue.get()
                    self.send(msg)
                    time.sleep(.1+sleep)
            except AttributeError:
                break

    def query(self, type, target=None, message=None):
        msg = type
        if target:
            msg += ' ' + target
        if message:
            while len(message) > 400:
                self.append(msg + ' :' + message[:400])
                message = message[400:]
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

class DogBotError(Exception):
    pass

def main():
    dog = DogBot()
    dog.add_connect(u'kanade.irc.ozinger.org', 6667)
    dog.start()

if __name__ == '__main__':
    main()