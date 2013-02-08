# -*- coding:utf-8 -*-

alias = [u'나이']

import time

def cmd_age(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 날짜를 기준으로 나이와 생일 정보를 출력해줍니다. 날짜는 YYYYMMDD 형식입니다. | usage: ?age YYYYMMDD | ?age YYYYMMDD YYYYMMDD (기준일 추가)'
        )
        return

    if ' ' in args:
        args, start = args.split(' ',1)
        now = time.strptime(start,'%Y%m%d')
    else:
        now = time.localtime()
        start = None

    nowtime = time.mktime(now)

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
    if now.tm_mon < data.tm_mon or (now.tm_mon == data.tm_mon and now.tm_mday < data.tm_mday):
        western_age -= 1

    res = u'%d년 %02d월 %02d일 출생자: '% (data.tm_year,data.tm_mon,data.tm_mday)
    if start:
        res += u'%d년 %02d월 %02d일 기준으로 ' % (now.tm_year,now.tm_mon,now.tm_mday)
    res += u'%d세 (만 %d세) | ' % (korean_age,western_age)

    days = int((nowtime - datatime)/86400)

    res += u'출생일로부터 '
    if start:
        res += u'기준일까지 '
    res += u'{:,}일 경과 | '.format(days)

    birth_temp = data
    birth = birth_temp.tm_yday - now.tm_yday
    if korean_age-western_age == 1:
        t = (birth_temp[0],12,31,birth_temp[3],birth_temp[4],birth_temp[5],birth_temp[6],birth_temp[7],birth_temp[8])
        lastday = time.localtime(time.mktime(t))
        birth += lastday.tm_yday


    if start:
        res += u'기준일로부터 '
    res += u'다음 생일까지 %d일 남음' % birth

    bot.con.query(
        'PRIVMSG',
        line.target,
        res
    )
