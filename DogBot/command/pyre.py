# -*- coding:utf-8 -*-

alias = ['pyre27', 'py27']
handler = []


def cmd_pyre(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Python 2.7 문서 링크 | usage: ?pyre library_name'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'http://docs.python.org/2.7/library/%s.html' % args
    )