# -*- coding:utf-8 -*-

alias = []
handler = []

from DogBot.system.error import *


def cmd_quit(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'으르렁…! 관리자만 사용가능한 명령어입니다.'
        )
        return
    if not args:
        args = 'QUIT'

    bot.con.query(
        'QUIT',
        args
    )
    bot.con.query(
        None
    )

    bot.running = False

    raise DogBotError('QUIT')