# -*- coding:utf-8 -*-

alias = []

def cmd_restart(bot, line, args):
    if line.login != 'item4':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 관리자만 사용가능한 명령어입니다.'
        )
        return
    if args is None:
        args = 'RESTART'

    bot.con.send(
        'QUIT ' + args
    )

    bot.running = False
    bot.restart = True
    bot.con.running = False

