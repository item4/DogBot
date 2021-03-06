# -*- coding:utf-8 -*-

alias = [u'애니시간표']
handler = []

#import xml.etree.ElementTree
import json
import urllib


def cmd_anitime(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'애니 편성 시간표를 출력합니다. | usage: ?anitime 요일 | (월, 화, 수, 목, 금, 토, 외, 신)'
        )
        return
    elif args in [u'일',u'일요일']:
        wday = 0
    elif args in [u'월',u'월요일']:
        wday = 1
    elif args in [u'화',u'화요일']:
        wday = 2
    elif args in [u'수',u'수요일']:
        wday = 3
    elif args in [u'목',u'목요일']:
        wday = 4
    elif args in [u'금',u'금요일']:
        wday = 5
    elif args in [u'토',u'토요일']:
        wday = 6
    elif args in [u'외',u'그외']:
        wday = 7
    elif args in [u'신',u'신작']:
        wday = 8
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍?'
        )
        return

    data = urllib.urlopen('http://www.anissia.net/anitime/list', urllib.urlencode({'w':wday})).read()
    data = data.decode('utf8')

    data = json.loads(data)

    res = ''
    
    if len(data) > 30:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 너무 길어요! 직접 가서 보세요 - http://www.anissia.net/anitime/'
        )
        return
    
    for x in data:
        time, title, genre = x['t'], x['s'], x['g']
        time = time[:2] + ':' + time[2:] if wday not in [7,8] else '20' + time[:2] + '-' + time[2:]

        res += '[%s] %s' % (time,title)
        if genre != '/':
            res += ' (%s)' % genre.replace(' ','')
        if len(res) >= 150:
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )
            res = ''
        else:
            res += ' | '

    if res:
        bot.con.query(
            'PRIVMSG',
            line.target,
            res[:-3]
        )
