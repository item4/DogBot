# -*- coding:utf-8 -*-

alias = [u'나이']
handler = []

from datetime import datetime


def cmd_age(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'입력받은 날짜를 기준으로 나이와 생일 정보를 출력해줍니다. 날짜는 YYYYMMDD 형식입니다. | usage: ?age YYYYMMDD | ?age YYYYMMDD YYYYMMDD (기준일 추가)'
        )
        return

    if ' ' in args:
        args, start = args.split(' ', 1)
        now = datetime.strptime(start, '%Y%m%d')
    else:
        now = datetime.now()
        start = None

    try:
        data = datetime.strptime(args, '%Y%m%d')
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 비정상적인 시간입력이에요! (YYYYMMDD 형식)'
        )
        return

    korean_age = now.year - data.year + 1
    western_age = now.year - data.year
    if now.month < data.month or (now.month == data.month and now.day < data.day):
        western_age -= 1

    res = u'%d년 %02d월 %02d일 출생자: ' % (data.year, data.month, data.day)
    if start:
        res += u'%d년 %02d월 %02d일 기준으로 ' % (now.year, now.month, now.day)
    res += u'%d세 (만 %d세) | ' % (korean_age, western_age)

    days = now.toordinal() - data.toordinal()

    res += u'출생일로부터 '
    if start:
        res += u'기준일까지 '
    res += u'{:,}일 경과 | '.format(days)

    temp = data.replace(datetime.today().year)
    birth = temp.toordinal() - now.toordinal()
    if birth < 1:
        temp = data.replace(datetime.today().year + 1)
        birth = temp.toordinal() - now.toordinal()

    if start:
        res += u'기준일로부터 '
    res += u'다음 생일까지 %d일 남음' % birth

    bot.con.query(
        'PRIVMSG',
        line.target,
        res
    )
