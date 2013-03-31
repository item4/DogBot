# -*- coding:utf-8 -*-

alias = [u'롤']
handler = []

import re
import urllib
import urllib2

def cmd_lol(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'리그 오브 레전드 소환사 검색기입니다. | usage: ?lol 소환사ID'
        )
        return

    url = 'http://op.gg/summoner/%s' % urllib.urlencode({'userName':args.encode('utf8')})
    try:
        data = urllib2.urlopen(url,None,3).read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! op.gg에 접속할 수 없습니다.'
        )
        return
    data = data.decode('utf8').replace('\r','').replace('\n','').replace('\t','')

    if u'찾을 수 없는 소환사입니다.' in data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'%s님은 찾을 수 없는 소환사입니다.' % args
        )
        return

    pattern = \
    r'<div class="summonerHeader[^>]+>'+\
    r'(?:<div class="summonerImage"><img [^>]+></div>)?'+\
    r'<div class="summonerRank">'+\
    r'<span class="ratingStatSummaryType">(.+?)</span>'+\
    r'<span class="tierRank">(.+?)</span>'+\
    r'(?:<span class="leaguePoints">(.+?)</span>)?'+\
    r'</div>'+\
    r'<h1 class="summonerName">([^<]+)'+\
    r'<a [^>]+><span class="summonerLadderRank">(.+?)</span></a></h1>'+\
    r'<div class="summonerSimpleInfo">'+\
    r'<div class="summonerNational">.+?</div>'+\
    r'<div class="summonerDash">&#151;</div>'+\
    ur'(?:<div class="summonerTeam tip" title="소속 팀">(.+?)</div><div class="summonerDash">&#151;</div>)?'+\
    r'(?:<div class="summonerLevel">(.+?)</div><div class="summonerDash">&#151;</div>)?'+\
    r'<div class="summonerExtra">(.+?)</div>'+\
    r'</div></div>'

    info = re.search(pattern,data)

    if info:
        res = u'[%s] %s' % (info.group(4),info.group(5)) # ID, 랭킹

        if info.group(6): # 팀
            res += u' | 소속 팀: ' + info.group(6)

        if info.group(7): # 레벨
            res += u' | ' + info.group(7)

        res += ' | ' + info.group(1) + ' ' + info.group(2)

        if info.group(3):
            res += ' | ' + info.group(3)

        if info.group(8):
            temp = info.group(8)
            temp = re.sub('</span><span[^>]+>', ', ', temp)
            res += ' | ' + re.sub('</?[^>]+>', '', temp)

        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )

    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 매칭에 실패했습니다. 관리자에게 문의해주세요.'
        )


