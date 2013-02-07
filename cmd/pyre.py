# -*- coding:utf-8 -*-

alias = []

def cmd_pyre(bot, line, args):
    if not args:
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'http://docs.python.org/library/%s.html' % args
    )