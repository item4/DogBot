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

    if not match:
        url = 'http://www.php.net/manual/kr/function.%s.php' % (path,)

    data = urllib.urlopen(url).read()
    data = data.decode('utf8', 'ignore').replace('\r', '').replace('\n', '')

    match = re.search(ur'<p class="verinfo">\(([^\)]+)\)</p><p class="refpurpose"><span class="refname">([^<]+)</span> &mdash; <span class="dc-title">([^<]+)</span>', data)
    if match:
        description = re.search('<div class="methodsynopsis dc-description">(.+?)</div>', data).group(1)
        description = re.sub(r'</?[^>]+>', '', description)
        description = re.sub('\s{2,}', ' ', description).strip()
        description = description.replace('&quot;', "'")

        msg = u'%s: %s (%s)' % (match.group(2).replace('&gt;', '>'),
                                match.group(3).replace('&#039;', "'").replace('&quot;', "'"),
                                match.group(1).replace('&gt;', '>'))

        warning = re.search('<div class="warning">\s*<strong class="warning">Warning</strong>\s*<p[^>]+>(.+?)</p>', data)

        if warning:
            warning = warning.group(1)
            if 'deprecated' in warning.lower():
                msg = '\x02[DEPRECATED]\x02 ' + msg + ' / Deprecated' +\
                 re.search('(?:<[^>]+>DEPRECATED</[^>]+>|deprecated)( as of PHP \d+\.\d+\.\d+)', data).group(1)
            else:
                msg = '\x02[WARNING]\x02 ' + msg

        bot.con.query(
            'PRIVMSG',
            line.target,
            msg
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
            u'멍멍! 그런 함수를 찾을 수 없어요.'
        )


def main():
    pass

if __name__ == '__main__':
    main()
