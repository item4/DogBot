# -*- coding: utf-8 -*-

alias = ['=',u'계산']

import re
import urllib
import urllib2

def cmd_calc(bot, line, args):
    if args is None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'구글 검색을 통해 계산을 수행합니다. | usage: ?= 1+2*3/4'
        )
        return

    try:
        data = urllib2.urlopen('https://www.google.co.kr/search?%s' % urllib.urlencode({'q':args+'='}),None,3).read()
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
    r'<div class="cwtlotc">\s<span class="cwcot" dir="ltr" id="cwos">(.+?)</span>'+\

    res = re.search(pattern,data)
    bot.con.query(
        'PRIVMSG',
        line.target,
        u'%s %s' % (res.group(1),res.group(2))
    )


def main():
    pass

if __name__ == '__main__':
    main()
