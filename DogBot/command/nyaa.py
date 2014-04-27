# -*- coding:utf-8 -*-

alias = [u'냐토렌트']
handler = []

import urllib
import re
import HTMLParser


def cmd_nyaa(bot, line, args):
    if args and args.startswith('-all '):
        cats = '0'
        args = args[5:]
    else:
        cats = '1_11'

    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'NyaaTorrents에서 Raw Anime를 검색해줍니다. | usage: ?nyaa inazuma | ?nyaa -all vanguard (전체 카테고리)'
        )
        return

    try:
        data = urllib.urlopen('http://www.nyaa.eu/?%s' % urllib.urlencode({'page':'search','cats':cats,'filter':0,'term':args.encode('u8')})).read()
    except IOError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 냐토렌트에 접속할 수 없어요.'
        )
        return
    data = data.decode('u8')
    match = re.finditer(r'<tr[^>]+><td[^>]+><a[^>]+><img[^>]+></a></td><td[^>]+><a[^>]+>(.+?)</a></td><td[^>]+><a href="([^"]+)"[^>]+><img[^>]+></a></td><td[^>]+>(.+?)</td>(?:<td[^>]+>(\d+)</td><td[^>]+>(\d+)</td>|<td class="tlistfailed" colspan="2">.+?</td>)<td[^>]+>(.+?)</td><td[^>]+>\d+</td></tr>', data)

    i = 1
    for x in match:
        res = u'%s (%s/S:%s/L:%s/DLs:%s) - %s' % (
            x.group(1),
            x.group(3),
            x.group(4),
            x.group(5),
            x.group(6),
            x.group(2)
        )
        res = HTMLParser.HTMLParser().unescape(res)
        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )
        i += 1
        if i > 3:
            break
        
    if i == 1:
        match = re.search('<td class="viewtorrentname">(.+?)</td>', data)
        if match:
            title = match.group(1)
            
            match = re.search('<td class="thead">Seeders:</td><td class="vtop">(.+?)</td></tr><tr><td class="thead">Tracker:</td><td>.+?</td><td class="thead">Leechers:</td><td class="vtop">(.+?)</td></tr><tr><td class="thead">Information:</td><td>.*?</td><td class="thead">Downloads:</td><td class="vtop">(.+?)</td></tr><tr><td class="thead">Stardom:</td><td>.+?</td><td class="thead">File size:</td><td class="vtop">(.+?)</td>', data)
            seeders = match.group(1)
            leechers = match.group(2)
            downloads = match.group(3)
            filesize = match.group(4)
            url = re.search('<div class="viewdownloadbutton"><a href="(.+?)" rel="nofollow"><img src="http://files.nyaa.se/www-download.png" alt="Download"></a>', data).group(1)
            
            res = u'%s (%s/S:%s/L:%s/DLs:%s) - %s' % (
                title,
                filesize,
                seeders,
                leechers,
                downloads,
                url
            )
            res = HTMLParser.HTMLParser().unescape(res)
            res = re.sub('</?[^>]+>', '', res)
            bot.con.query(
                'PRIVMSG',
                line.target,
                res
            )
        else:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! 검색 결과가 없어요!'
            )