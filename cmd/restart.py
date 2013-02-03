# -*- coding:utf-8 -*-

alias = []

def cmd_restart(bot, line, args):
    if line.login != 'item4':
        return
    if args is None:
        args = 'RESTART'

    bot.con.send(
        'QUIT ' + args
    )

    bot.running = False
    bot.restart = True
    bot.con.running = False

