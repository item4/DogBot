# -*- coding: utf-8 -*-

alias = ['=',u'계산']
handler = []

import re
import urllib
import urllib2

def cmd_calc(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'구글 검색을 통해 계산을 수행합니다. | usage: ?= 1+2*3/4'
        )
        return

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17')]

    try:
        data = opener.open('https://www.google.co.kr/search?%s' % urllib.urlencode({'q':args+'='}),None,3).read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 구글 접속에 실패했습니다.'
        )
        return

    data = data.decode('utf8')

    pattern = r'<div class="cwed">\s<div class="cwled">\s<div id="cwfleb"></div>\s'+\
    r'<div class="cwletbl" id="cwletbl">\s<div class="cwleotc">\s'+\
    r'<span class="cwclet" id="cwles">(.+?)</span>\s</div>\s</div>\s</div>\s'+\
    r'<div class="cwtld">\s<div class="cwtlb" id="cwtlbb"></div>\s'+\
    r'<div class="cwtlwm"></div>\s<div class="cwtltbl" id="cwotbl">\s'+\
    r'<div id="cwtltblr" tabindex="0">\s<div class="cwtlptc"></div>\s'+\
    r'<div class="cwtlotc">\s<span class="cwcot" dir="ltr" id="cwos">(.+?)</span>'

    res = re.search(pattern,data)

    if res:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'%s %s' % (res.group(1).strip().replace(u'\xa0',','),res.group(2).strip())
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 수식이 잘못되었거나 계산할 수 없어요.'
        )


def main():
    pass

if __name__ == '__main__':
    main()
