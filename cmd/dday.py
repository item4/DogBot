# -*- coding: utf-8 -*-

alias = []

import time

def cmd_dday(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'해당 날짜까지 며칠 남았는지, 혹은 며칠 지났는지 계산합니다. | usage: ?dday 20131231'
        )
        return

    try:
        dday = time.mktime(time.strptime(args,'%Y%m%d'))
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 날짜가 올바른 형식이 아닙니다.'
        )
        return

    today = time.localtime()
    day = (today[0],today[1],today[2],0,0,0,today[6],today[7],today[8])
    dday -= time.mktime(day)

    if dday > 0:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'{0}까지 {1:,}일 남았습니다.'.format(time.strftime('%Y-%m-%d',day),int(dday//86400))
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'{0}로부터 {1:,}일 지났습니다.'.format(time.strftime('%Y-%m-%d',day),int(-dday//86400))
        )