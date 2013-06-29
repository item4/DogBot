# -*- coding:utf-8 -*-

alias = [u'부재']
handler = ['PRIVMSG','QUIT']

import cmd

import time

from utility.time import read_time

def cmd_busy(bot, line, args):
    if not args:
        args = u'그냥'

    bot.db['busy'][line.nick] = (args,time.time())
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s, 부재중으로 설정합니다. (이유: %s)' % (line.nick, args)
    )

def on_PRIVMSG(bot, line):
    print repr(cmd)
    for x in bot.db['busy'].keys():
        reason, busytime = bot.db['busy'].get(x)
        busytime = time.time() - busytime

        if line.nick == x:
            bot.con.query(
                u'PRIVMSG',
                line.target,
                u'%s, 부재를 해지합니다. (%s 동안 부재였음.)' % (x,read_time(busytime))
            )
            del bot.db['busy'][x]

        elif line.message.startswith(x) and x in bot.db['channel'][line.target]['member']:

            bot.con.query(
                u'PRIVMSG',
                line.target,
                u'%s, %s님은 %s 전부터 부재중입니다. (이유: %s)' % (line.nick,x,read_time(busytime),reason)
            )
    return cmd.KEEP

def on_QUIT(bot, line):
    if line.nick in bot.db['busy']:
        del bot.db['busy'][line.nick]

    return cmd.KEEP