# -*- coding:utf-8 -*-

alias = ['jee']
handler = []

import urllib
import re


def cmd_javaee(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Java EE7기준 Method의 API 문서 링크를 알려줍니다. (대소문자 구분 안함) | usgae: ?javaee Action'
        )
        return

    data = urllib.urlopen('http://docs.oracle.com/javaee/7/api/allclasses-noframe.html').read().decode('u8')

    matches = re.findall('<li><a href="([^"]+)" title="([^"]+)">(?:<i>)?((?i)%s.*?)(?:</i>)?</a></li>' % args, data)

    if matches:
        for match in matches:
            bot.con.query(
                'PRIVMSG',
                line.target,
                match[2] + ': ' + match[1] + ' - http://docs.oracle.com/javaee/7/api/' + match[0]
            )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 찾을 수 없어요!'
        )