# -*- coding:utf-8 -*-

alias = [u'부재']

import time

def cmd_busy(bot, line, args):
    if not args:
        args = u'그냥'

    bot.db['busy'][line.nick] = (args,time.time())
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s, 부재중으로 설정합니다. (이유: %s)' % (line.nick, args)
    )