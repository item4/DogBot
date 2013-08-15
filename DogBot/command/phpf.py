# -*- coding:utf-8 -*-

alias = [u'pf']
handler = []

import urllib
import re


def cmd_phpf(bot, line, args):
    if not args:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'PHP 함수의 정보를 보여줍니다. | usgae: ?phpf function_name'
        )
        return

    path = args.replace('::', '.')

    url = 'http://php.net/%s' % (path,)

    data = urllib.urlopen(url).read()
    data = data.decode('utf8', 'ignore').replace('\r', '').replace('\n', '')

    match = re.search(ur'<p class="verinfo">\(([^\)]+)\)</p><p class="refpurpose"><span class="refname">([^<]+)</span> &mdash; <span class="dc-title">([^<]+)</span>', data)

    if match:
        description = re.search('<div class="methodsynopsis dc-description">(.+?)</div>', data).group(1)
        description = re.sub(r'</?[^>]+>', '', description)
        description = re.sub('\s{2,}', ' ', description).strip()
        description = description.replace('&quot;', "'")

        bot.con.query(
            'PRIVMSG',
            line.target,
            u'\x02%s\x02: %s (%s)' % (match.group(2).replace('&gt;', '>'),
                                    match.group(3).replace('&#039;', "'").replace('&quot;', "'"),
                                    match.group(1).replace('&gt;', '>'))
        )
        bot.con.query(
            'PRIVMSG',
            line.target,
            description
        )
        bot.con.query(
            'PRIVMSG',
            line.target,
            url
        )

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
