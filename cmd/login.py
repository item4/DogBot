# -*- coding:utf-8 -*-
alias=[u'로그인']

def cmd_login(bot, line, args):
    bot.con.query(
        'WHOIS',
        line.nick
    )