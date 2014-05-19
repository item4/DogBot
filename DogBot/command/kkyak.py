# -*- coding:utf-8 -*-

alias = [u'꺆']
handler = []


def cmd_kkyak(bot, line, args):
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s, 꺆' % line.nick
    )