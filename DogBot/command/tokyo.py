# -*- coding:utf-8 -*-

alias = [u'도쿄도','tokyotosho']
handler = []


import urllib
import re


def cmd_tokyo(bot, line, args):
    if args and args.startswith('-all '):
        search_type = 0
        args = args[5:]
    else:
        search_type = 7

    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Tokyo Toshokan(도쿄도서관)에서 Raws를 검색해줍니다. | usage: ?tokyo inazuma | ?tokyo -all vanguard (전체 카테고리)'
        )
        return

    url = 'http://www.tokyotosho.info/search.php?%s' % urllib.urlencode({'terms':args.encode('utf8'),'type':search_type})

    try:
        data = urllib.urlopen(url).read()
    except IOError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 도쿄도서관에 접속할 수 없어요!'
        )
        return
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.finditer(r'<tr[^>]+><td[^>]+><a[^>]+><span[^>]+></span></a></td><td[^>]+><a[^>]+><span[^>]+></span></a> <a rel="nofollow" type="application/x-bittorrent" href="([^"]+)">(.+?)</a></td><td[^>]+>(?:<a[^>]+>Website</a> \| )?<a[^>]+>Details</a></td></tr><tr[^>]+><td[^>]+>(?:Authorized: <span class="auth_ok">Yes</span> )?Submitter: (?:<a[^>]+>.*?</a>|Anonymous) \| Size: ([^\|]+) \| Date: ([^\|]+)(?: \| Comment: .*?)?</td><td[^>]+>S: <span[^>]+>(\d+)</span> L: <span[^>]+>(\d+)</span> C: <span[^>]+>(\d+)</span> ID: \d+</td></tr>',data)

    i = 1
    for x in data:
        res=u'%s (%s/%s/S:%s/L:%s/C:%s) - %s' % (\
            x.group(2).replace('<span class="s"> </span>',''),\
            x.group(3),x.group(4),x.group(5),x.group(6),\
            x.group(7),x.group(1).replace('&amp;','&'))
        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )
        i += 1
        if i > 3:
            break
    
    if i == 1:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 검색결과가 없어요.'
        )