# -*- coding:utf-8 -*-

alias = [r'롤']

import re
import urllib

def cmd_lol(bot, line, args):
    if not args:
        return
    url = 'http://op.gg/summoner/%s' % urllib.urlencode({'userName':args.encode('utf8')})

    data = urllib.urlopen(url).read()
    data = data.decode('utf8').replace('\r','').replace('\n','').replace('\t','')

    if u'찾을 수 없는 소환사입니다.' in data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'%s은(는) 찾을 수 없는 소환사입니다.' % args
        )
        return

    pattern = '<tr[^>]+><th>(.+?)</th>'+\
    '<td><span[^>]+>(.+?)</span></td>'+\
    '<td[^>]*><span[^>]+>(.+?)</span></td>'+\
    '<td>(?:<span[^>]+>)?([^<]+)(?:</span>)?</td>'+\
    '<td>(?:-|<span[^>]+>(.+?)</span>/<span[^>]+>(.+?)</span>)</td>'+\
    '<td><span[^>]+>(.+?)</span></td>'+\
    '<td>(?:<span[^>]+>([^<]+)</span>\s*/\s*)?<span[^>]+>([^<]+)</span></td>'+\
    '<td>(?:<span[^>]+>([^<]+)</span>\s*/\s*)?<span[^>]+>([^<]+)</span></td>'+\
    '<td>(?:<span class="kills average tip" title="([^"]+)">([^<]+)</span>\s*/\s*)?<span class="kills total tip" title="([^"]+)">(.+?)</span></td>'+\
    '<td>(?:<span[^>]+>([^<]+)</span>\s*/\s*)?<span[^>]+>([^<]+)</span></td>'

    stat = re.findall(pattern,data)

    info = re.search('<div class="summonerName">([^<]+)</div><div class="summonerSimpleInfo"><div class="summonerNational">([^<]+)</div><div class="summonerDash">&#151;</div><div class="summonerLevel">([^<]+)</div>',data)

    bot.con.query(
        'PRIVMSG',
        line.target,
        u'\x02%s\x02 (%s/%s)' % (info.group(1),info.group(2),info.group(3))
    )
    for l in stat:
        print l
        res = '\x02' + l[0] + '\x02:: ' # 게임 종류

        res += u'%s승, %s패' % (l[1],l[2]) # 승/패

        if l[3] != '-': # 승률
            res += ' (' + l[3] + ')'
        res += ' | '

        if l[4] != '-': # 레이팅
            res += u'레이팅 - 탑:%s, 현재:%s | ' % (l[4],l[5])

        res += u'탈주:%s | ' % l[6] # 탈주

        res += u'챔피언킬:' + l[8]
        if l[7]:
            res += u' (평균 ' + l[7] + ')'
        res += ' | '

        res += u'어시스트:' + l[10]
        if l[9]:
            res += u' (평균 ' + l[9] + ')'
        res += ' | '

        res += u'미니언킬:' + l[14] + '(' + l[13].replace(' ','') + ')'
        if l[11]:
            res += u', 평균 ' + l[12] + '(' + l[11].replace(' ','') + ')'
        res += ' | '

        res += u'타워:' + l[16]
        if l[15]:
            res += u' (평균 ' + l[15] + ')'
        #res += ' | '

        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )




