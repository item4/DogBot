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

    args = args.replace('$', '')
    path = args.replace('::', '.')
    superclass, func = args.replace('_', '-').split('::') if '::' in args else ('function', args)
    if args.startswith('mysqli_stmt_'):
        superclass = 'mysqli-stmt'
        func = args[12:].replace('_', '-')
    elif args.startswith('mysqli_'):
        superclass = 'mysqli'
        func = args[7:].replace('_', '-')
    param = dict(path=path, superclass=superclass, func=func)

    urls = ['http://www.php.net/manual/en/{superclass}.{func}.php', 'http://php.net/{path}']
    match = None

    while not match and len(urls) > 0:
        url = urls.pop().format(**param)
    
        data = urllib.urlopen(url).read()
        data = data.decode('u8', 'ignore').replace('\r', '').replace('\n', '')
    
        match = re.search(ur'<p class="verinfo">\(([^\)]+)\)</p><p class="refpurpose"><span class="refname">(.+?)</span> &mdash; <span class="dc-title">(.+?)</span>', data)

    if match:
        descriptions = re.findall('<div class="(?:method|constructor)synopsis dc-description">(.+?)</div>', data)

        msg = u'%s: %s (%s)' % (match.group(2).replace('&gt;', '>').replace('</span> -- <span class="refname">', ' / '),
                                re.sub(r'</?[^>]+>', '', match.group(3)).replace('&#039;', "'").replace('&quot;', "'"),
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
        for description in descriptions:
            description = re.sub(r'</?[^>]+>', '', description)
            description = re.sub('\s{2,}', ' ', description).strip()
            description = description.replace('&quot;', "'")
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
            u'멍멍! 그런 함수를 찾을 수 없어요!'
        )