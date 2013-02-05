# -*- coding:utf-8 -*-

alias = [u'나이']

import time

def cmd_age(bot, line, args):
    if not args:
        return

    if ' ' in args:
        args, start = args.split(' ',1)
        now = time.strptime(start,'%Y%m%d')
    else:
        now = time.localtime()
        start = None

    try:
        data = time.strptime(args,'%Y%m%d')
        datatime = time.mktime(data)
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'비정상적인 시간입력. (YYYYMMDD)'
        )
        return

    korean_age = now.tm_year - data.tm_year + 1
    western_age = now.tm_year - data.tm_year
    if now.tm_mon < data.tm_mon or (now.tm_mon >= data.tm_mon and now.tm_mday < data.tm_mday):
        western_age -= 1

    res = u'%d년 %02d월 %02d일 출생자: '% (data.tm_year,data.tm_mon,data.tm_mday)
    if start:
        res += u'%d년 %02d월 %02d일 기준으로 ' % (now.tm_year,now.tm_mon,now.tm_mday)
    res += u'%d세 (만 %d세)' % (korean_age,western_age)
    bot.con.query(
        'PRIVMSG',
        line.target,
        res
    )
