# -*- coding:utf-8 -*-

alias = []
handler = []

import urllib
import re

def cmd_html(bot, line, args):
    if args is None:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'HTML Tag의 정보를 보여줍니다. | usgae: ?html tag_name | ex) ?html strong'
        )
        return

    args = args.lower()

    if args in ['h1','h2','h3','h4','h5','h6']:
        tag = '&lt;h1&gt;,&lt;h2&gt;,&lt;h3&gt;,&lt;h4&gt;,&lt;h5&gt;,&lt;h6&gt;'
    else:
        tag = '&lt;%s&gt;' % args

    data = urllib.urlopen('https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5/HTML5_element_list').read()
    data = data.decode('utf8').replace('\r','').replace('\n','')
    data = re.search(r'<td><a href="([^"]+)"(?: title="([^"]+)")?><code>%s</code></a>( <a href="/en-US/docs/HTML/HTML5">.+?</a>)?</td>\s*<td>(.+?)</td>' % tag,data)

    if not data:
        bot.con.query(
            'PRIVMSG',
            line.target,
            u'멍멍! 그런 HTML Tag는 목록에 없어요.'
        )
    else:
        description = data.group(2) if data.group(2) else re.sub('</?[^>]+>', '', data.group(4))
        if data.group(3):
            description = '[HTML5] ' + description
        description = description.replace('&lt;', '<').replace('&gt;', '>')
        bot.con.query(
            'PRIVMSG',
            line.target,
            description
        )
        bot.con.query(
            'PRIVMSG',
            line.target,
            'https://developer.mozilla.org' + data.group(1)
        )

def main():
    pass

if __name__ == '__main__':
    main()
