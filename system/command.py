# -*- coding: utf-8 -*-

__all__ = ['DogBotCommand']

import os
import sys
import types

import cmd
import utility

from system.error import *
from utility.time import read_time

class DogBotCommand(object):
    def __init__(self, bot):
        self.cmdlist = {}
        self.syscmd = ['load','reload','list']
        self.bot = bot
        self.reload()

    def reload(self, cmdname=None):
        if cmdname is None:
            self.bot.del_handler_all()
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

                handler = list(module.handler) # 임시 땜빵.

                for x in handler:
                    self.bot.del_handler(x, cmdname)

                return self._load(cmdname)
            else:
                raise DogBotError(u'로딩된적 없는 명령어')

    def load(self, cmdname=None):
        if cmdname not in self.cmdlist:
            return self._load(cmdname)
        else:
            raise DogBotError(u'이미 로딩된 명령어')

    """def _load(self, cmdname):
        modname = ".".join(["cmd", cmdname])
        print 'SYS: Load ' + modname

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
                func = getattr(module,'cmd_%s' % cmdname)
                func._dogbot_modname = modname
                self.cmdlist[aliasname] = func

            handler = list(module.handler) # 임시 땜빵.
            for x in handler:
                self.bot.add_handler(x, cmdname, getattr(module,'on_%s' % x))
                print 'SYS: Link handler %s-%s' % (cmdname, x)

            return 1
        """
    def _load(self, cmdname):
        try:
            print 'SYS: Load command.' + cmdname

            tmp_module = types.ModuleType('cmd_'+cmdname)

            #tmp_module.__dict__['cmd'] = __import__('cmd')
            #tmp_module.__dict__['utility'] = utility

            execfile('./cmd/' + cmdname + '.py', tmp_module.__dict__, tmp_module.__dict__)

            func = tmp_module.__dict__.get('cmd_' + cmdname)

            self.cmdlist[cmdname] = func

            alias = list(tmp_module.__dict__.get('alias'))
            for x in alias:
                self.cmdlist[x] = func

            handler = list(tmp_module.__dict__.get('handler'))
            for x in handler:
                self.bot.add_handler(x, cmdname, tmp_module.__dict__.get('on_%s' % x))
                print 'SYS: Link handler %s-%s' % (cmdname, x)

            return 1
        except Exception as e:
            print 'SYS: Load cmd.' + cmdname + ' failed'
            print u'%s: %s' % (e.__class__.__name__,e)
            return 0

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
                u'으르렁…!! 관리자만 사용가능한 명령어입니다.'
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
                u'으르렁…!! 관리자만 사용가능한 명령어입니다.'
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
        if res:
            bot.con.query(
                'PRIVMSG',
                line.target,
                res[1:]
            )


def main():
    pass

if __name__ == '__main__':
    main()
