# -*- coding:utf-8 -*-

alias = []

def cmd_quit(bot, line, args):
    if line.login != 'item4':
        return
    if args is None:
        args = 'QUIT'

    bot.con.send(
        'QUIT ' + args
    )

    bot.running = False
    bot.con.running = False

    raise DogBotError('QUIT')