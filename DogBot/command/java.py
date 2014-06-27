# -*- coding:utf-8 -*-

alias = ['jse','jse8']
handler = []

import urllib
import re


def cmd_java(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'Java Method의 API 문서 링크를 알려줍니다. (대소문자 구분 안함) | usgae: ?java Runnable'
        )
        return

    data = urllib.urlopen('http://docs.oracle.com/javase/8/docs/api/allclasses-noframe.html').read().decode('u8')

    matches = re.findall('<li><a href="([^"]+)" title="([^"]+)">(?:<span[^>]+>)?((?i)%s.*?)(?:</span>)?</a></li>' % args, data)

    if matches:
        for match in matches:
            bot.con.query(
                'PRIVMSG',
                line.target,
                match[2] + ': ' + match[1] + ' - http://docs.oracle.com/javase/8/docs/api/' + match[0]
            )
    else:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 찾을 수 없어요!'
        )