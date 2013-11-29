# -*- coding:utf-8 -*-

alias = [u'자막']
handler = []

import json
import urllib
import re

wday = [u'일', u'월', u'화', u'수', u'목', u'금', u'토']


def cmd_sub(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'애니 자막 현황을 출력합니다. | usage: ?sub 이나즈마 일레븐'
        )
        return

    end = False
    find_item = None 
    for i in xrange(7):
        data = urllib.urlopen('http://www.anissia.net/anitime/list', urllib.urlencode({'w':str(i)})).read()
        data = data.decode('utf8')

        data = json.loads(data)

        for x in data:
            if args.lower() in x['s'].lower():
                find_item = x
                end = True
                break

        if end:
            break

    if not find_item:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 그런 애니를 찾을 수 없어요!'
        )
        return
    data = urllib.urlopen('http://www.anissia.net/anitime/cap', urllib.urlencode({'i':find_item['i']})).read()
    data = data.decode('u8')
    data = json.loads(data)

    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 그런 애니를 찾을 수 없어요!'
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[%s] %s - http://%s' %
            (wday[i], find_item['s'], find_item['l'])
        )
        for l in data:
            ep = int(l['s'])
            if ep % 10 == 0:
                ep = '{0:02d}'.format(int(ep/10))
            else:
                temp = divmod(ep/10.,1)
                ep = '{0:03d}{1:s}'.format(int(temp[0]),str(temp[1])[0])
            month = l['d'][4:6]
            day = l['d'][6:8]
            hour = l['d'][8:10]
            minute = l['d'][10:12]
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'#%s %s - http://%s (%s.%s %s:%s)' %
                 (ep, l['n'], l['a'], month, day, hour, minute)
            )
