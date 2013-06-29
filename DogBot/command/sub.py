# -*- coding:utf-8 -*-

alias = [u'자막']
handler = []

import urllib
import re

def cmd_sub(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'애니 자막 현황을 출력합니다. | usage: ?anitime 이나즈마 일레븐'
        )
        return

    end = False
    for i in xrange(6):
        data = urllib.urlopen('http://gs.saro.me/api/aw' + str(i)).read()
        data = data.decode('utf8')

        #tree = xml.etree.ElementTree.fromstring(data)

        data = re.findall('<n t="[^"]+" s="([^"]+)"/>',data)

        for x in data:
            if args in x:
                args = x
                end = True
                break

        if end:
            break

    data = urllib.urlopen('http://gs.saro.me/api/as?s=' + urllib.quote(args.encode('u8'))).read()
    data = data.decode('utf8')

    if data == '<r v=""/>':
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 그런 애니를 찾을 수 없어요!'
        )
    else:
        data = data[6:-3].split('|')[1:]
        for l in data:
            temp, nick, url = l.split(',')
            ep = temp[:3]
            month = temp[3:5]
            day = temp[5:7]
            hour = temp[7:9]
            minute = temp[9:11]
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'#%s %s - http://%s (%s.%s %s:%s)' % (ep, nick, url, month, day, hour, minute)
            )

