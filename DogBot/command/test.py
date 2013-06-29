# -*- coding:utf-8 -*-

alias = []
handler = ['PRIVMSG']

from DogBot import command

def cmd_test(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'으르렁…! 관리자만 사용가능한 명령어입니다.'
        )
        return

def on_PRIVMSG(bot, line):
    if line.message == u'멍?':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍?'
        )
        return command.STOP