# -*- coding:utf-8 -*-

alias = ['pyre3', 'py3', 'py34']
handler = []


def cmd_pyre34(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Python 3.4 문서 링크 | usage: ?py34 library_name'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'http://docs.python.org/3.4/library/%s.html' % args
    )