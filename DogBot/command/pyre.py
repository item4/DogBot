# -*- coding:utf-8 -*-

alias = []
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
        u'http://docs.python.org/2/library/%s.html' % args
    )