# -*- coding:utf-8 -*-

alias = []
handler = []


def cmd_ping(bot, line, args):
    bot.con.query(
        'PRIVMSG',
        line.target,
        '%s, pong!' % line.nick
    )