# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import re


isup_pattern = re.compile('<a href="([^"]+)" class="domain">')


def cmd_isup(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'http://isup.me 사이트를 통해 입력된 사이트가 접속 가능한지 검사합니다. | usage: ?isup item4.net'
        )
        return

    if args.startswith('http://'):
        args = args[7:]

    data = urllib.urlopen('http://www.isup.me/%s' % args).read().decode('u8')

    url = isup_pattern.search(data)
    if url:
        con = u'가능' if 'is up' in data else u'불가'
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'[%s] 접속 %s' % (url.group(1).replace('&#x2F;', '/'), con)
        )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍?'
        )