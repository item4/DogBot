# -*- coding: utf-8 -*-

__all__ = ['DogBotCommand']

import os
import sys

from system.error import *
from utility.time import read_time

class DogBotCommand:
    def __init__(self):
        self.cmdlist = {}
        self.syscmd = ['load','reload','list']
        self.reload()

    def reload(self, cmdname=None):
        if cmdname is None:
            self.cmdlist.clear()
            os.chdir('./')
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
            return self._load(cmdname)
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
                        u'%s: %s' % (e.__class__.__name__,e.decode('cp949'))
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
                temp = self.load(args)
            except Exception as e:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    u'%s 명령어 로드 실패 - %s: %s' % (args,e.__class__.__name__,e)
                )
            else:
                if temp == 0:
                    bot.con.query(
                        'PRIVMSG',
                        line.target,
                        u'%s 명령어 로드 실패 (존재하지 않는 명령어)' % args
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
        check = False
        cmd = self.cmdlist.keys()+self.syscmd
        res = ''
        for x in cmd:
            res += ' ?' + x
            if len(res) > 150:
                bot.con.query(
                    'PRIVMSG',
                    line.target,
                    res[1:]
                )
                res = ''


def main():
    pass

if __name__ == '__main__':
    main()
