# -*- coding:utf-8 -*-

alias = []

def cmd_exit(bot, line, args):
    if line.login != 'item4':
        return
    if args is None:
        args = 'EXIT Program'

    bot.con.send(
        'QUIT ' + args
    )

    bot.running = False
    bot.con.running = False
    bot.system.running = False
    bot.system.exit_reason = args