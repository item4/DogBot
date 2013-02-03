# -*- coding:utf-8 -*-

alias = []

import time

def cmd_exit(bot, line, args):
    if line.login != 'item4':
        return
    bot.running = False
    bot.con.query(
        'EXIT',
        args
    )
    time.sleep(.5)

    bot.con.running = False
    bot.system.running = False