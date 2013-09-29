# -*- coding:utf-8 -*-

alias = [u'냐토렌트']
handler = []

import urllib
import re
import HTMLParser


def cmd_nyaa(bot, line, args):
    if args.startswith('-all '):
        cats = '0'
        args = args[5:]
    else:
        cats = '1_11'

    try:
        data = urllib.urlopen('http://www.nyaa.eu/?%s' % urllib.urlencode({'page':'search','cats':cats,'filter':0,'term':args.encode('utf8') if args else ''})).read()
    except IOError:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'timeout'
        )
        return
    data = data.decode('utf8')
    data = re.finditer(r'<tr[^>]+><td[^>]+><a[^>]+><img[^>]+></a></td><td[^>]+><a[^>]+>(.+?)</a></td><td[^>]+><a href="([^"]+)"[^>]+><img[^>]+></a></td><td[^>]+>(.+?)</td>(?:<td[^>]+>(\d+)</td><td[^>]+>(\d+)</td>|<td class="tlistfailed" colspan="2">.+?</td>)<td[^>]+>(\d+)</td><td[^>]+>\d+</td></tr>',data)
    """


    """
    i = 1
    for x in data:

        res=u'%s (%s/S:%s/L:%s/DLs:%s) - %s' % (
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
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'그런거 없다'
        )




def main():
    pass

if __name__ == '__main__':
    main()
