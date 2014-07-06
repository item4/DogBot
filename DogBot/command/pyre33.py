# -*- coding:utf-8 -*-

alias = ['py33']
handler = []


def cmd_pyre33(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Python 3.3 문서 링크 | usage: ?py33 library_name'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'http://docs.python.org/3.3/library/%s.html' % args
    )