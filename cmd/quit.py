# -*- coding:utf-8 -*-

alias = []

import time

def cmd_quit(bot, line, args):
    if line.login != 'item4':
        return
    bot.running = False
    bot.con.query(
        'QUIT',
        args
    )
    time.sleep(.5)

    bot.con.running = False