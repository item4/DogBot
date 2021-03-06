# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import urllib2
import re
import HTMLParser


content_type_pattern = re.compile('Content-Type: (.+)')
charset_pattern1 = re.compile('charset=(.+)')
charset_pattern2 = re.compile('charset=["\']?([^"\'/]+)[^"\']?')


def cmd_web(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'웹페이지의 내용을 간략히 보여줍니다. | usgae: ?web url'
        )
        return

    if not args.startswith('http://') and not args.startswith('https://'):
        args = 'http://' + args
    try:
        obj = urllib2.urlopen(args, None, 3)
        data = obj.read()
    except:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 접속에 실패하였습니다!'
        )
        return

    header = str(obj.info())

    content_type = content_type_pattern.search(header)

    if not content_type or not content_type.group(1).startswith('text/'):
        bot.con.query(
            'PRIVMSG',
            line.target,
            '[%s] non-text content: %s' % (args, content_type.group(1))
        )
        return

    test = charset_pattern1.search(header)
    if not test:
        test = charset_pattern2.search(data)

    if test:
        charset = test.group(1)
    else:
        charset = 'u8'

    charset = charset.lower()

    if charset == 'euc-kr':
        charset = 'cp949'
    elif charset == 'utf-8':
        charset = 'u8'

    try:
        data = data.decode(charset, 'replace') # 'cp949')
    except:
        try:
            data = data.decode('u8', 'replace')
        except:
            bot.con.query(
                'PRIVMSG',
                line.target,
                u'멍멍! charset 감지에 실패하였습니다!'
            )
            return

    data = HTMLParser.HTMLParser().unescape(data)
    data = data.replace('\n', ' ').replace('\r', ' ')
    data = re.sub(r'\s{2,}', ' ', data)
    data = re.sub(r'<(style|script|title)[^>]*>.*?</\1>', '' ,data, flags=re.I|re.S)
    data = re.sub(r'</?[^>]+>', '', data)
    data = re.sub(r'\s{2,}', ' ', data)

    data = data.strip()

    if len(data) > 150:
        data = data[:150]
    elif not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! frameset 페이지거나 페이지 내용이 없습니다!'
        )
        return

    bot.con.query(
        'PRIVMSG',
        line.target,
        '[%s] %s' % (args, data)
    )