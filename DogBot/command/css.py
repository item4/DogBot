# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import re


def cmd_css(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'CSS 속성의 정보를 보여줍니다. | usgae: ?css attribute_name'
        )
        return

    args = args.lower()

    if args in [':after',':before',':first-letter',':first-line']:
        args = ':%s (%s)' % (args,args)

    args = args.replace('<', '&lt;').replace('>', '&gt;').replace('(', '\(').replace(')', '\)')

    data = urllib.urlopen('https://developer.mozilla.org/en-US/docs/Web/CSS/Reference').read()
    data = data.decode('u8').replace('\r', '').replace('\n', '')
    data = re.search(r'<li><a (class="new" )?href="([^"]+)" title=""><code>%s</code></a>' % args,data)

    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 해당하는 CSS를 찾을 수 없어요!'
        )
    else:
        res = u'{%s} - ' % args.replace('&lt;', '<').replace('&gt;', '>').replace('\(', '(').replace('\)', ')')

        if data.group(1):
            res += u'MDN에 문서가 제작되지 않음'
        else:
            res += u'https://developer.mozilla.org%s' % data.group(2)
        bot.con.query(
            'PRIVMSG',
            line.target,
            res
        )