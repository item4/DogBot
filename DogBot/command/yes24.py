# -*- coding:utf-8 -*-

alias = [u'책']
handler = []

import urllib
import re


book_pattern = re.compile(
    '<td class="goods_infogrp">\s*' +
    '<p class="goods_name goods_icon">\s*(\[.+?\])\s*<a href="([^"]+)"><strong>(.+?)</strong></a>\s*' +
    '<span class="goods_sname">(.+?)</span>\s*' +
    '(?:<img[^>]+>&nbsp;)?\s*' +
    '</p>\s*<p class="goods_info">.+?</p>\s*' +
    u'<p class="goods_price">\s*[0-9,]+원 → <strong>([0-9,]+원)</strong>',
    re.S
)


def cmd_yes24(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'YES24에서 상품을 검색합니다. | usgae: ?yes24 소드 아트 온라인'
        )
        return

    param = urllib.urlencode({'domain': 'ALL', 'query': args.encode('cp949'), 'scode': '002'})
    data = urllib.urlopen('http://www.yes24.com/SearchCorner/Search?%s' % param).read().decode('cp949')

    matches = book_pattern.findall(data)

    if matches:
        i = 0
        for match in matches:
            bot.con.query(
                'PRIVMSG',
                line.target,
                match[0] + ' ' + chr(2) + match[2] + chr(2) + ': ' + match[3].strip() +\
                ' (' + match[4] + ') - http://www.yes24.com' + match[1]
            )
            if i > 1:
                break
            else:
                i += 1
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 찾을 수 없어요!'
        )