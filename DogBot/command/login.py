# -*- coding:utf-8 -*-

alias = [u'로그인']
handler = ['330','NICK','QUIT']

from DogBot import command


def cmd_login(bot, line, args):
    bot.con.query(
        'WHOIS',
        line.nick
    )


def on_330(bot, line): # whois login
    _, nick, id = line.target.split(' ')

    bot.login[nick] = id

    bot.con.query(
        u'NOTICE',
        nick,
        u'로그인 되었습니다.'
    )

    return command.KEEP


def on_NICK(bot, line): # change nick
    temp = bot.login.get(line.nick)

    if temp:
        del bot.login[line.nick]
        bot.login[line.message] = temp

    return command.KEEP


def on_QUIT(bot, line):
    if line.nick in bot.login:
        del bot.login[line.nick]

    return command.KEEP